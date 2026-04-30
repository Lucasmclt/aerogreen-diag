import plotly.graph_objects as go
import streamlit as st


def render_emissions_bar_chart(df):
    palette = ["#6366f1", "#8b5cf6", "#06b6d4", "#10b981", "#f59e0b", "#ef4444", "#14b8a6", "#64748b", "#ec4899"]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["Catégorie"],
        y=df["Émissions (kg CO₂e)"],
        text=[f"{v:.0f} kg" for v in df["Émissions (kg CO₂e)"]],
        textposition="outside",
        marker=dict(
            color=palette[:len(df)],
            line=dict(width=0)
        ),
        hovertemplate="<b>%{x}</b><br>%{y:.2f} kg CO₂e<extra></extra>"
    ))

    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=45, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=13, color="#111827"),
        xaxis=dict(showgrid=False, title="", tickangle=-15),
        yaxis=dict(showgrid=True, gridcolor="#eef2f7", title="kg CO₂e"),
        bargap=0.32,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


def render_score_radar(score_rows):
    fig = go.Figure()

    categories = score_rows["Pilier"].tolist()
    values = score_rows["Score"].tolist()

    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name="Score AeroGreen",
        line=dict(color="#6366f1"),
        fillcolor="rgba(99,102,241,0.18)"
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="white",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="#e5e7eb",
                tickfont=dict(size=10)
            ),
            angularaxis=dict(gridcolor="#e5e7eb")
        ),
        showlegend=False,
        height=420,
        margin=dict(l=30, r=30, t=30, b=30),
        paper_bgcolor="white",
        font=dict(color="#111827")
    )

    st.plotly_chart(fig, use_container_width=True)


def render_score_bars(score_rows):
    colors = []
    for score in score_rows["Score"]:
        if score < 33:
            colors.append("#ef4444")
        elif score < 66:
            colors.append("#f59e0b")
        else:
            colors.append("#10b981")

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=score_rows["Pilier"],
        x=score_rows["Score"],
        orientation="h",
        text=[f"{v:.0f}/100" for v in score_rows["Score"]],
        textposition="outside",
        marker=dict(color=colors),
        hovertemplate="<b>%{y}</b><br>%{x:.0f}/100<extra></extra>"
    ))

    fig.update_layout(
        height=340,
        margin=dict(l=20, r=50, t=20, b=20),
        xaxis=dict(range=[0, 100], showgrid=True, gridcolor="#eef2f7", title=""),
        yaxis=dict(title=""),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=13, color="#111827"),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
