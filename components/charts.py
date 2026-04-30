import plotly.graph_objects as go
import streamlit as st


def render_emissions_bar_chart(df):
    colors = ["#6366f1", "#8b5cf6", "#06b6d4", "#10b981"]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["Catégorie"],
        y=df["Émissions (kg CO₂e)"],
        text=[f"{v:.0f} kg" for v in df["Émissions (kg CO₂e)"]],
        textposition="outside",
        marker=dict(
            color=colors,
            line=dict(width=0)
        ),
        hovertemplate="<b>%{x}</b><br>%{y:.2f} kg CO₂e<extra></extra>"
    ))

    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=13, color="#111827"),
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(showgrid=True, gridcolor="#eef2f7", title="kg CO₂e"),
        bargap=0.35
    )

    st.plotly_chart(fig, use_container_width=True)
