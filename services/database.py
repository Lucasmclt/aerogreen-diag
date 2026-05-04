import json
import secrets
import hashlib
import hmac
import sqlite3
from datetime import datetime
from pathlib import Path


DB_DIR = Path("data")
DB_PATH = DB_DIR / "aerogreen.db"

PBKDF2_ITERATIONS = 210_000
HASH_ALGORITHM = "sha256"


def _code_exists(conn, table: str, code: str) -> bool:
    row = conn.execute(f"SELECT 1 FROM {table} WHERE public_code = ?", (code,)).fetchone()
    return row is not None


def _new_public_code(conn, table: str, prefix: str) -> str:
    while True:
        code = f"{prefix}-" + secrets.token_hex(4).upper()
        if not _code_exists(conn, table, code):
            return code


def _backfill_public_codes(conn, table: str, prefix: str) -> None:
    rows = conn.execute(
        f"SELECT id FROM {table} WHERE public_code IS NULL OR TRIM(public_code) = ''"
    ).fetchall()
    for row in rows:
        conn.execute(
            f"UPDATE {table} SET public_code = ? WHERE id = ?",
            (_new_public_code(conn, table, prefix), row["id"]),
        )


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
            public_code TEXT UNIQUE,
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
        _ensure_audits_public_code_column(conn)


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

    return {"id": row["id"], "email": row["email"]}


def get_or_create_passwordless_user(email: str) -> dict:
    """Create or return a local demo user used by the portfolio prototype."""
    email = email.strip().lower()

    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, email FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if row is not None:
            return {"id": row["id"], "email": row["email"]}

        random_password = secrets.token_urlsafe(48)
        password_hash, salt = _hash_password(random_password)

        cursor = conn.execute(
            """
            INSERT INTO users (email, password_hash, salt, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (email, password_hash, salt, datetime.utcnow().isoformat())
        )

        return {"id": int(cursor.lastrowid), "email": email}


def _ensure_audits_public_code_column(conn):
    columns = [row["name"] for row in conn.execute("PRAGMA table_info(audits);").fetchall()]
    if "public_code" not in columns:
        conn.execute("ALTER TABLE audits ADD COLUMN public_code TEXT;")
    _backfill_public_codes(conn, "audits", "DIAG")
    conn.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_audits_public_code
    ON audits(public_code);
    """)


def _generate_unique_audit_code(conn) -> str:
    _ensure_audits_public_code_column(conn)
    return _new_public_code(conn, "audits", "DIAG")


def save_audit(user_id: int, company: dict, fit_score: float, fit_result: str, inputs: dict, result: dict) -> str:
    result_safe = _make_json_safe(result)

    with get_connection() as conn:
        public_code = _generate_unique_audit_code(conn)
        conn.execute(
            """
            INSERT INTO audits (
                public_code, user_id, company_name, company_city, company_sector, client_reference, contact_name,
                fit_score, fit_result, global_score, grade, risk_label, total_tonnes,
                inputs_json, result_json, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                public_code,
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
        return public_code


def list_audits(user_id: int) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, public_code, company_name, company_city, company_sector, client_reference,
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


def get_audit_by_public_code(user_id: int, public_code: str) -> dict | None:
    code = (public_code or "").strip()
    if not code:
        return None

    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM audits
            WHERE public_code = ? AND user_id = ?
            """,
            (code, user_id)
        ).fetchone()

    if row is None:
        return None

    data = dict(row)
    data["inputs"] = json.loads(data["inputs_json"])
    data["result"] = json.loads(data["result_json"])
    return data


def get_latest_audit(user_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id
            FROM audits
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (user_id,)
        ).fetchone()

    if row is None:
        return None
    return get_audit(user_id, int(row["id"]))


def audit_public_code_exists(user_id: int, public_code: str) -> bool:
    return get_audit_by_public_code(user_id, public_code) is not None


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
