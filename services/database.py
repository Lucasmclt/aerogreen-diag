import os
import sqlite3
import secrets
import hashlib
import hmac
import json
from datetime import datetime
from pathlib import Path


DB_DIR = Path("data")
DB_PATH = DB_DIR / "aerogreen.db"

PBKDF2_ITERATIONS = 210_000
HASH_ALGORITHM = "sha256"


def get_connection():
    DB_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA busy_timeout = 5000;")
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE COLLATE NOCASE,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS audits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            company_name TEXT NOT NULL,
            company_city TEXT,
            company_sector TEXT,
            client_reference TEXT,
            contact_name TEXT,
            fit_score REAL DEFAULT 0,
            fit_result TEXT,
            global_score REAL,
            grade TEXT,
            risk_label TEXT,
            total_tonnes REAL,
            inputs_json TEXT NOT NULL,
            result_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_audits_user_created
        ON audits(user_id, created_at DESC);
        """)


def _hash_password(password: str, salt_hex: str | None = None) -> tuple[str, str]:
    if salt_hex is None:
        salt = secrets.token_bytes(32)
        salt_hex = salt.hex()
    else:
        salt = bytes.fromhex(salt_hex)

    password_hash = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS
    ).hex()

    return password_hash, salt_hex


def create_user(email: str, password: str) -> tuple[bool, str]:
    email = email.strip().lower()

    if not email or "@" not in email:
        return False, "Adresse email invalide."

    if len(password) < 10:
        return False, "Le mot de passe doit contenir au moins 10 caractères."

    password_hash, salt = _hash_password(password)

    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO users (email, password_hash, salt, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (email, password_hash, salt, datetime.utcnow().isoformat())
            )
        return True, "Compte créé."
    except sqlite3.IntegrityError:
        return False, "Un compte existe déjà avec cette adresse."


def authenticate_user(email: str, password: str) -> dict | None:
    email = email.strip().lower()

    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, email, password_hash, salt FROM users WHERE email = ?",
            (email,)
        ).fetchone()

    if row is None:
        return None

    candidate_hash, _ = _hash_password(password, row["salt"])

    if not hmac.compare_digest(candidate_hash, row["password_hash"]):
        return None

    return {
        "id": row["id"],
        "email": row["email"],
    }


def save_audit(user_id: int, company: dict, fit_score: float, fit_result: str, inputs: dict, result: dict) -> int:
    result_safe = _make_json_safe(result)

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO audits (
                user_id, company_name, company_city, company_sector, client_reference, contact_name,
                fit_score, fit_result, global_score, grade, risk_label, total_tonnes,
                inputs_json, result_json, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                company.get("company_name", "Entreprise non renseignée"),
                company.get("company_city", ""),
                company.get("company_sector", ""),
                company.get("client_reference", ""),
                company.get("contact_name", ""),
                float(fit_score or 0),
                fit_result or "",
                float(result.get("global_score", 0)),
                result.get("grade", ""),
                result.get("risk_label", ""),
                float(result.get("total_tonnes", 0)),
                json.dumps(_make_json_safe(inputs), ensure_ascii=False),
                json.dumps(result_safe, ensure_ascii=False),
                datetime.utcnow().isoformat()
            )
        )
        return int(cursor.lastrowid)


def list_audits(user_id: int) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, company_name, company_city, company_sector, client_reference,
                   fit_score, global_score, grade, risk_label, total_tonnes, created_at
            FROM audits
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,)
        ).fetchall()

    return [dict(row) for row in rows]


def get_audit(user_id: int, audit_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM audits
            WHERE id = ? AND user_id = ?
            """,
            (audit_id, user_id)
        ).fetchone()

    if row is None:
        return None

    data = dict(row)
    data["inputs"] = json.loads(data["inputs_json"])
    data["result"] = json.loads(data["result_json"])
    return data


def delete_audit(user_id: int, audit_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM audits WHERE id = ? AND user_id = ?",
            (audit_id, user_id)
        )
        return cursor.rowcount > 0


def _make_json_safe(value):
    try:
        import pandas as pd
        if isinstance(value, pd.DataFrame):
            return value.to_dict(orient="records")
    except Exception:
        pass

    if isinstance(value, dict):
        return {str(k): _make_json_safe(v) for k, v in value.items()}

    if isinstance(value, list):
        return [_make_json_safe(v) for v in value]

    if isinstance(value, tuple):
        return [_make_json_safe(v) for v in value]

    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass

    return value
