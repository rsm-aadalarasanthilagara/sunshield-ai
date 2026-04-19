"""
SunShield AI — Streamlit MVP
Run: streamlit run src/frontend/app.py
"""

import glob
import json
import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv
from google import genai as google_genai

load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.env")
)

st.set_page_config(
    page_title="SunShield AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)


_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(_HERE, "../data/processed/ucsd_sites_scored.csv")

# ── Design System tokens ──────────────────────────────────────────────────────
GREEN = "#0B3D2E"
SAGE = "#A7D7C5"
GOLD = "#F4C542"
BG = "#FFFCE8"  # pale warm yellow
CARD = "#FFFFFF"
TEXT = "#1A1A1A"
MUTED = "#555555"
SUBTLE = "#888888"
BORDER = "#A7D7C5"
BORDER2 = "#E8F5F0"
SB_BG = "#C8E6D4"  # distinct sage green sidebar

SITE_LABELS = {
    "parking_structure": "Parking Structures",
    "plaza": "Plazas",
    "walkway": "Walkways",
    "remote": "Remote Areas",
}


# ── CSS (Design System) ───────────────────────────────────────────────────────
def inject_css() -> None:
    st.markdown(
        f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        *, html, body {{ font-family: 'Inter', sans-serif !important; }}
        .main p, .main span, .main label, .main div {{ color: {TEXT}; }}

        /* Page */
        .stApp, .main, [data-testid="stAppViewContainer"] {{
            background-color: {BG} !important;
        }}

        /* ── Centered page layout ── */
        .main .block-container,
        [data-testid="stAppViewBlockContainer"] {{
            max-width: 1100px !important;
            padding-left: 20px !important;
            padding-right: 20px !important;
            padding-top: 1.5rem !important;
            margin-left: auto !important;
            margin-right: auto !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }}
        @media (max-width: 1140px) {{
            .main .block-container,
            [data-testid="stAppViewBlockContainer"] {{
                padding-left: 32px !important;
                padding-right: 32px !important;
            }}
        }}
        @media (max-width: 768px) {{
            .main .block-container,
            [data-testid="stAppViewBlockContainer"] {{
                padding-left: 16px !important;
                padding-right: 16px !important;
            }}
        }}

        /* Budget box — unified card containing the slider */
        .budget-card {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-left: 5px solid {GREEN};
            border-radius: 16px;
            padding: 20px 24px 16px 24px;
            box-shadow: 0 2px 8px rgba(11,61,46,0.08);
            margin-bottom: 16px;
        }}

        /* ── All buttons: base reset ── */
        div.stButton > button,
        div.stDownloadButton > button {{
            border-radius: 10px !important;
            padding: 0.45rem 1.2rem !important;
            font-size: 0.875rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.01em !important;
            transition: background-color 0.2s ease, border-color 0.2s ease,
                        box-shadow 0.2s ease, transform 0.15s ease !important;
            cursor: pointer !important;
        }}

        /* ── Primary buttons — dark green fill ── */
        div.stButton > button[data-testid="baseButton-primary"] {{
            background-color: {GREEN} !important;
            color: #FFFFFF !important;
            border: none !important;
            box-shadow: 0 1px 4px rgba(11,61,46,0.20) !important;
        }}
        div.stButton > button[data-testid="baseButton-primary"]:hover {{
            background-color: #1a5c43 !important;
            box-shadow: 0 4px 14px rgba(11,61,46,0.30) !important;
            transform: translateY(-1px) !important;
        }}
        div.stButton > button[data-testid="baseButton-primary"]:active {{
            background-color: #0a3028 !important;
            transform: translateY(0) !important;
            box-shadow: none !important;
        }}

        /* ── Secondary / default buttons — white with green border ── */
        div.stButton > button[data-testid="baseButton-secondary"],
        div.stButton > button:not([data-testid="baseButton-primary"]) {{
            background-color: #FFFFFF !important;
            color: {GREEN} !important;
            border: 1.5px solid {BORDER} !important;
            box-shadow: 0 1px 3px rgba(11,61,46,0.08) !important;
        }}
        div.stButton > button[data-testid="baseButton-secondary"]:hover,
        div.stButton > button:not([data-testid="baseButton-primary"]):hover {{
            background-color: #F0FAF5 !important;
            border-color: {GREEN} !important;
            box-shadow: 0 3px 10px rgba(11,61,46,0.15) !important;
            transform: translateY(-1px) !important;
        }}
        div.stButton > button[data-testid="baseButton-secondary"]:active,
        div.stButton > button:not([data-testid="baseButton-primary"]):active {{
            background-color: #dff0ea !important;
            transform: translateY(0) !important;
        }}

        /* ── Text inside buttons: always inherit parent colour ── */
        div.stButton > button * {{ color: inherit !important; }}

        /* ── Download buttons — force white/green, override Streamlit dark default ── */
        [data-testid="stDownloadButton"] button,
        div.stDownloadButton button,
        [data-testid="stDownloadButton"] > button,
        div.stDownloadButton > button {{
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            color: {GREEN} !important;
            border: 1.5px solid {BORDER} !important;
            box-shadow: 0 1px 3px rgba(11,61,46,0.08) !important;
        }}
        [data-testid="stDownloadButton"] button:hover,
        div.stDownloadButton button:hover {{
            background-color: #F0FAF5 !important;
            background: #F0FAF5 !important;
            border-color: {GREEN} !important;
            box-shadow: 0 3px 10px rgba(11,61,46,0.15) !important;
            transform: translateY(-1px) !important;
        }}
        [data-testid="stDownloadButton"] button:active,
        div.stDownloadButton button:active {{
            background-color: #dff0ea !important;
            background: #dff0ea !important;
            transform: translateY(0) !important;
        }}
        [data-testid="stDownloadButton"] button *,
        div.stDownloadButton button * {{
            color: {GREEN} !important;
        }}

        /* ── Disabled buttons ── */
        div.stButton > button:disabled,
        div.stDownloadButton > button:disabled {{
            opacity: 0.45 !important;
            cursor: not-allowed !important;
            transform: none !important;
            box-shadow: none !important;
        }}

        /* ── Tooltip / help hover text ── */
        div[role="tooltip"] {{
            background-color: {GREEN} !important;
            border-radius: 8px !important;
            padding: 6px 10px !important;
            box-shadow: 0 4px 12px rgba(11,61,46,0.25) !important;
            max-width: 240px !important;
        }}
        div[role="tooltip"],
        div[role="tooltip"] p,
        div[role="tooltip"] span,
        div[role="tooltip"] div,
        div[role="tooltip"] small,
        div[role="tooltip"] * {{
            color: #FFFFFF !important;
            font-size: 0.78rem !important;
            font-weight: 400 !important;
            line-height: 1.4 !important;
            background-color: transparent !important;
        }}
        div[role="tooltip"] {{ background-color: {GREEN} !important; }}


        /* Alerts */
        [data-testid="stAlert"] p,
        [data-testid="stAlert"] span,
        [data-testid="stAlert"] div {{ color: {TEXT} !important; }}

        /* Markdown text */
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] strong {{ color: {TEXT} !important; }}

        /* Captions */
        [data-testid="stCaptionContainer"] p,
        .stCaption p {{ color: {MUTED} !important; font-size: 0.8rem !important; }}

        /* Dataframe */
        [data-testid="stDataFrame"] {{
            border-radius: 12px !important;
            border: 1px solid {BORDER} !important;
            overflow: hidden !important;
        }}

        /* Scrollbar */
        ::-webkit-scrollbar {{ width: 5px; }}
        ::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 3px; }}

        /* Hide Streamlit chrome */
        #MainMenu, footer {{ visibility: hidden; }}
        [data-testid="stToolbar"] {{ display: none; }}

        /* ── Custom components ── */
        .hero {{
            background: linear-gradient(135deg, {GREEN} 0%, #1a5c43 100%);
            border-radius: 16px;
            padding: 24px 32px;
            margin-bottom: 24px;
            box-shadow: 0 8px 24px rgba(11,61,46,0.16);
        }}
        .hero h1 {{ color: #FFE566 !important; font-size: 2rem; font-weight: 800; margin: 0; }}
        .hero p  {{ color: #C8EED8 !important; font-size: 0.95rem; margin: 6px 0 0; }}
        .hero small {{ color: rgba(200,238,216,0.7) !important; font-size: 0.72rem; display:block; margin-top: 10px; }}
        .hero * {{ color: inherit !important; }}

        .insight-box {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-left: 5px solid {GREEN};
            border-radius: 16px;
            padding: 20px 24px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(11,61,46,0.08);
        }}
        .insight-label {{
            font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
            letter-spacing: 0.6px; color: {MUTED}; margin-bottom: 8px;
        }}
        .insight-text {{
            color: {TEXT}; font-size: 0.97rem; line-height: 1.7; font-weight: 500;
        }}

        .kpi-row {{
            display: grid; grid-template-columns: repeat(4,1fr);
            gap: 16px; margin-bottom: 24px;
        }}
        .kpi-card {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 20px 18px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(11,61,46,0.08);
            transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
        }}
        .kpi-card:hover {{
            box-shadow: 0 8px 24px rgba(11,61,46,0.16);
            transform: translateY(-2px);
        }}
        .kpi-label {{ color: {MUTED}; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
        .kpi-value {{ color: {GREEN}; font-size: 1.7rem; font-weight: 800; margin: 6px 0 2px; line-height: 1.1; }}
        .kpi-sub   {{ color: {SUBTLE}; font-size: 0.7rem; }}

        .sec-title {{
            font-size: 1rem; font-weight: 700; color: {GREEN};
            border-bottom: 2px solid {BORDER};
            padding-bottom: 8px; margin: 24px 0 12px;
        }}

        .site-card {{
            background: {CARD};
            border: 1px solid {BORDER2};
            border-left: 4px solid {GREEN};
            border-radius: 16px;
            padding: 20px 24px;
            margin-bottom: 10px;
            box-shadow: 0 2px 8px rgba(11,61,46,0.08);
            transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
        }}
        .site-card:hover {{
            box-shadow: 0 8px 24px rgba(11,61,46,0.16);
            border-color: {BORDER};
        }}
        .site-card.top {{ border-left: 4px solid {GOLD}; }}
        .site-rank  {{ color: {GOLD}; font-weight: 800; font-size: 1.1rem; }}
        .site-name  {{ color: {GREEN}; font-weight: 700; font-size: 0.97rem; }}
        .score-pill {{
            background: {GREEN}; color: {GOLD};
            border-radius: 20px; padding: 3px 12px;
            font-size: 0.82rem; font-weight: 700;
        }}
        .top-badge {{
            background: {GOLD}; color: {GREEN};
            border-radius: 10px; padding: 2px 9px;
            font-size: 0.62rem; font-weight: 800;
            text-transform: uppercase; margin-right: 6px;
        }}
        .why-label {{
            font-size: 0.7rem; font-weight: 700; color: {MUTED};
            text-transform: uppercase; letter-spacing: 0.4px; margin-bottom: 6px;
        }}
        .why-bullet {{ color: {TEXT}; font-size: 0.85rem; line-height: 1.8; }}
        .breakdown-wrap {{
            background: {BORDER2}; border-radius: 10px;
            padding: 14px 18px; margin-bottom: 8px;
        }}
        .bar-label {{ width:130px; font-size:0.73rem; color:{MUTED}; flex-shrink:0; }}
        .bar-track {{ flex:1; background:#D5EDE4; border-radius:4px; height:7px; }}
        .bar-val   {{ width:34px; text-align:right; font-size:0.73rem; font-weight:700; color:{GREEN}; }}
    </style>
    """,
        unsafe_allow_html=True,
    )


# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["has_grid_access"] = df["has_grid_access"].astype(str).str.lower() == "true"
    df["site_type_label"] = df["site_type"].map(SITE_LABELS).fillna(df["site_type"])
    return df


RAW_DIR = os.path.join(_HERE, "../data/raw")


@st.cache_data
def load_heatmap_data() -> pd.DataFrame:
    files = glob.glob(os.path.join(RAW_DIR, "*.txt"))
    frames = []
    for f in files:
        try:
            df = pd.read_csv(
                f,
                sep=r"\s+",
                header=None,
                names=["time", "lat", "lon", "alt", "temp_c", "rh"],
            )
            df["source"] = os.path.basename(f)
            frames.append(df)
        except Exception:
            pass
    if not frames:
        return pd.DataFrame()
    combined = pd.concat(frames, ignore_index=True)
    # Filter to UCSD campus bounds (mirror MATLAB filter)
    combined = combined[
        (combined["lat"] >= 32.0)
        & (combined["lat"] <= 34.0)
        & (combined["lon"] >= -117.30)
        & (combined["lon"] <= -117.10)
    ].dropna(subset=["lat", "lon", "temp_c"])
    return combined.reset_index(drop=True)


def build_heatmap(hdf: pd.DataFrame) -> go.Figure:
    t_min, t_max = hdf["temp_c"].min(), hdf["temp_c"].max()
    hover = (
        "Temp: "
        + hdf["temp_c"].round(2).astype(str)
        + " °C<br>"
        + "RH: "
        + hdf["rh"].round(1).astype(str)
        + " %<br>"
        + "Alt: "
        + hdf["alt"].round(1).astype(str)
        + " m<br>"
        + hdf["source"]
    )
    fig = go.Figure(
        go.Scattermap(
            lat=hdf["lat"],
            lon=hdf["lon"],
            mode="markers",
            marker=dict(
                size=6,
                color=hdf["temp_c"],
                colorscale=[
                    [0.0, "#A7D7C5"],  # cool  → sage green
                    [0.4, "#F4C542"],  # warm  → gold
                    [0.75, "#E07B39"],  # hot   → orange
                    [1.0, "#C0392B"],  # hottest → red
                ],
                cmin=t_min,
                cmax=t_max,
                opacity=0.8,
                colorbar=dict(
                    title=dict(text="°C", side="right"),
                    thickness=12,
                    len=0.6,
                    tickfont=dict(color=TEXT, size=11),
                ),
            ),
            text=hover,
            hovertemplate="%{text}<extra></extra>",
            name="Temperature readings",
        )
    )
    fig.update_layout(
        map=dict(
            style="open-street-map", center=dict(lat=32.878, lon=-117.235), zoom=14
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=460,
        paper_bgcolor=BG,
        legend=dict(
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor=BORDER,
            borderwidth=1,
            font=dict(color=TEXT, size=11),
        ),
    )
    return fig


def greedy_select(df: pd.DataFrame, budget: float) -> pd.DataFrame:
    ranked = df.sort_values("dual_benefit_score", ascending=False)
    selected, spent = [], 0.0
    for _, row in ranked.iterrows():
        if spent + row["installation_cost"] <= budget:
            selected.append(row)
            spent += row["installation_cost"]
    return pd.DataFrame(selected).reset_index(drop=True) if selected else pd.DataFrame()


# ── Map ───────────────────────────────────────────────────────────────────────
def build_map(df: pd.DataFrame, selected_ids: set) -> go.Figure:
    df = df.copy()
    df["selected"] = df["site_id"].isin(selected_ids)
    df["hover"] = (
        "<b>"
        + df["name"]
        + "</b><br>"
        + "Score: "
        + df["dual_benefit_score"].round(1).astype(str)
        + "/100<br>"
        + "Cost: $"
        + df["installation_cost"].apply(lambda x: f"{x:,.0f}")
        + "<br>"
        + "People/day: "
        + df["pedestrians_per_day"].astype(str)
        + "<br>"
        + "kWh/yr: "
        + df["estimated_kwh_per_year"].apply(lambda x: f"{x:,.0f}")
    )
    unsel = df[~df["selected"]]
    sel = df[df["selected"]]
    fig = go.Figure()

    if not unsel.empty:
        # Lighter purple shaded by score: low=pale lavender, high=medium purple
        score_norm = (
            unsel["dual_benefit_score"] - unsel["dual_benefit_score"].min()
        ) / (
            (unsel["dual_benefit_score"].max() - unsel["dual_benefit_score"].min()) or 1
        )
        dot_colors = score_norm.apply(
            lambda v: (
                f"rgba({int(210 - v * 60)},{int(180 - v * 80)},{int(240 - v * 40)},0.85)"
            )
        ).tolist()
        fig.add_trace(
            go.Scattermap(
                lat=unsel["latitude"],
                lon=unsel["longitude"],
                mode="markers",
                marker=dict(size=10, color=dot_colors, opacity=0.9),
                text=unsel["hover"],
                hovertemplate="%{text}<extra></extra>",
                name="Other candidates",
            )
        )
    if not sel.empty:
        fig.add_trace(
            go.Scattermap(  # halo
                lat=sel["latitude"],
                lon=sel["longitude"],
                mode="markers",
                marker=dict(size=36, color="#6A0DAD", opacity=0.20),
                hoverinfo="skip",
                showlegend=False,
                name="_halo",
            )
        )
        fig.add_trace(
            go.Scattermap(  # selected dot + sun label
                lat=sel["latitude"],
                lon=sel["longitude"],
                mode="markers+text",
                marker=dict(size=20, color="#6A0DAD", opacity=1.0),
                text="☀️ " + sel["name"].str.split().str[:2].str.join(" "),
                textposition="top center",
                hovertext=sel["hover"],
                hovertemplate="%{hovertext}<extra></extra>",
                name="Selected sites",
            )
        )

    fig.update_layout(
        map=dict(
            style="open-street-map", center=dict(lat=32.878, lon=-117.235), zoom=14
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=430,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.01,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor=BORDER,
            borderwidth=1,
            font=dict(color=TEXT, size=11),
        ),
        paper_bgcolor=BG,
    )
    return fig


# ── AI helpers ────────────────────────────────────────────────────────────────
def _gemini(prompt: str) -> str | None:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    try:
        client = google_genai.Client(api_key=api_key)
        return client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        ).text
    except Exception:
        return None


def build_insight(selected: pd.DataFrame, budget: float) -> str:
    if selected.empty:
        return f"No sites fit within ${budget:,.0f}. Try increasing the budget."
    top = selected.iloc[0]
    spent = selected["installation_cost"].sum()
    people = int(selected["pedestrians_per_day"].sum())
    n = len(selected)
    remaining = budget - spent
    top_reason = max(
        [
            ("heat risk", top["heat_risk_score"]),
            ("solar potential", top["solar_potential_score"]),
            ("foot traffic", top["public_impact_score"]),
        ],
        key=lambda x: x[1],
    )[0]
    result = _gemini(
        f"You are SunShield AI. Write ONE paragraph, 3 sentences max, under 65 words, "
        f"for a campus facilities manager. Budget ${budget:,.0f}. Selected {n} sites. "
        f"Spent ${spent:,.0f}. Remaining ${remaining:,.0f}. "
        f"People protected {people:,}/day. Top site: {top['name']} "
        f"(score {top['dual_benefit_score']:.1f}, +{top['temp_delta']:.1f}°C above average, "
        f"${top['installation_cost']:,}). Be specific. Start with the budget amount. No jargon."
    )
    if result:
        return result.strip()
    note = (
        f"${remaining:,.0f} remaining" if remaining > 2000 else "budget fully utilized"
    )
    return (
        f"With ${budget:,.0f}, you can protect {people:,} people daily across {n} high-priority sites. "
        f"{top['name']} is your top pick — scoring {top['dual_benefit_score']:.1f}/100 with outstanding "
        f"{top_reason} (+{top['temp_delta']:.1f}°C above average, {top['pedestrians_per_day']} people/day). "
        f"Total spend: ${spent:,.0f} ({note})."
    )


def build_grant(site: pd.Series) -> str:
    result = _gemini(
        f"Write a 3-sentence grant justification for a solar shade canopy at {site['name']} at UCSD. "
        f"Score {site['dual_benefit_score']:.1f}/100, +{site['temp_delta']:.1f}°C above average, "
        f"{site['pedestrians_per_day']} people/day, {site['estimated_kwh_per_year']:,.0f} kWh/year, "
        f"${site['installation_cost']:,} cost. Persuasive, specific, under 80 words."
    )
    if result:
        return result.strip()
    return (
        f"{site['name']} records {site['temp_delta']:.1f}°C above campus average while serving "
        f"{site['pedestrians_per_day']} people daily — a critical climate intervention point. "
        f"The solar shade canopy will generate {site['estimated_kwh_per_year']:,.0f} kWh/year, "
        f"offsetting its ${site['installation_cost']:,} cost through energy savings. "
        f"This investment protects public health and advances UCSD's 2030 climate goals."
    )


# ── Card helpers ──────────────────────────────────────────────────────────────
def why_bullets_html(row: pd.Series) -> str:
    temp_f = row["temp_delta"] * 9 / 5
    cost_note = (
        "cost-effective" if row["installation_cost"] < 33_000 else "within budget"
    )
    items = [
        f"🌡️ <b>Hottest spot</b> — {temp_f:.1f}°F above campus average (urgent heat risk)",
        f"👥 <b>High traffic</b> — {row['pedestrians_per_day']:,} people/day benefit directly",
        f"☀️ <b>Strong solar</b> — generates {row['estimated_kwh_per_year']:,.0f} kWh/year",
        f"💰 <b>Investment</b> — ${row['installation_cost']:,} ({cost_note})",
    ]
    return "".join(f'<div class="why-bullet">• {i}</div>' for i in items)


def bar_html(label: str, val: float, color: str, weight: str) -> str:
    return (
        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;">'
        f'<span class="bar-label">{label} <span style="color:{SUBTLE};font-size:0.68rem;">({weight})</span></span>'
        f'<div class="bar-track"><div style="width:{val:.0f}%;background:{color};height:7px;border-radius:4px;"></div></div>'
        f'<span class="bar-val">{val:.1f}</span>'
        f"</div>"
    )


def _card_header(title: str) -> None:
    st.markdown(
        f'<div style="background:{GREEN};color:#FFFFFF;font-weight:700;font-size:0.95rem;'
        f'padding:12px 20px;border-radius:12px 12px 0 0;margin-bottom:0;letter-spacing:0.01em;">'
        f'{title}</div>',
        unsafe_allow_html=True,
    )


def _card_open() -> None:
    st.markdown(
        f'<div style="background:{CARD};border:1px solid {BORDER};border-top:none;'
        f'border-radius:0 0 12px 12px;padding:20px 24px;margin-bottom:16px;'
        f'box-shadow:0 2px 8px rgba(11,61,46,0.08);">',
        unsafe_allow_html=True,
    )


def _card_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


# ── Static sections (formerly expanders) ──────────────────────────────────────
def render_whatif(df: pd.DataFrame, budget: float, selected: pd.DataFrame) -> None:
    _card_header("🎯 What-If Scenarios")
    _card_open()
    if True:
        c1, c2 = st.columns(2)
        with c1:
            nb = budget + 50_000
            boosted = greedy_select(df, nb)
            new_sites = (
                []
                if selected.empty
                else [
                    r["name"]
                    for _, r in boosted.iterrows()
                    if r["site_id"] not in set(selected["site_id"])
                ]
            )
            st.markdown(
                f'<div style="font-weight:700;color:{GREEN};margin-bottom:8px;">What if budget increases to ${nb:,.0f}?</div>',
                unsafe_allow_html=True,
            )
            if new_sites:
                ep = int(boosted["pedestrians_per_day"].sum()) - (
                    int(selected["pedestrians_per_day"].sum())
                    if not selected.empty
                    else 0
                )
                ek = boosted["estimated_kwh_per_year"].sum() - (
                    selected["estimated_kwh_per_year"].sum()
                    if not selected.empty
                    else 0
                )
                st.success(
                    f"→ +{len(new_sites)} site(s): {', '.join(new_sites[:2])}\n\n→ +{ep:,} more people protected\n\n→ +{ek:,.0f} more kWh/year"
                )
            else:
                st.info("→ No additional sites fit even with $50k more")

        with c2:
            st.markdown(
                f'<div style="font-weight:700;color:{GREEN};margin-bottom:8px;">What if I skip the top site?</div>',
                unsafe_allow_html=True,
            )
            if not selected.empty:
                top_id = selected.iloc[0]["site_id"]
                alt_df = df[df["site_id"] != top_id].copy()
                alt = greedy_select(alt_df, budget)
                if not alt.empty:
                    next_best = alt.iloc[0]
                    st.info(
                        f"→ Next best: **{next_best['name']}** (Score: {next_best['dual_benefit_score']:.1f})\n\n"
                        f"→ {next_best['pedestrians_per_day']} people/day · ${next_best['installation_cost']:,}"
                    )
    _card_close()


def render_deepdive(selected: pd.DataFrame) -> None:
    _card_header("📈 Data Deep Dive")
    _card_open()
    if selected.empty:
        st.info("No sites selected.")
        _card_close()
        return
    cols = [
        "name", "dual_benefit_score", "heat_risk_score", "solar_potential_score",
        "public_impact_score", "feasibility_score", "installation_cost",
        "pedestrians_per_day", "estimated_kwh_per_year", "sun_hours_daily",
    ]
    tdf = selected[cols].copy()
    for c in ["dual_benefit_score","heat_risk_score","solar_potential_score",
              "public_impact_score","feasibility_score"]:
        tdf[c] = tdf[c].round(1)
    tdf = tdf.rename(columns={
        "dual_benefit_score": "Score", "heat_risk_score": "Heat",
        "solar_potential_score": "Solar", "public_impact_score": "Impact",
        "feasibility_score": "Feasibility", "installation_cost": "Cost ($)",
        "pedestrians_per_day": "People/Day", "estimated_kwh_per_year": "kWh/Yr",
        "sun_hours_daily": "Sun Hrs",
    })
    st.dataframe(
        tdf, width="stretch", hide_index=True,
        column_config={
            "Score":       st.column_config.NumberColumn(format="%.1f"),
            "Heat":        st.column_config.NumberColumn(format="%.1f"),
            "Solar":       st.column_config.NumberColumn(format="%.1f"),
            "Impact":      st.column_config.NumberColumn(format="%.1f"),
            "Feasibility": st.column_config.NumberColumn(format="%.1f"),
            "Cost ($)":    st.column_config.NumberColumn(format="$%d"),
            "kWh/Yr":      st.column_config.NumberColumn(format="%d"),
            "Sun Hrs":     st.column_config.NumberColumn(format="%.2f"),
        },
    )
    st.caption("Scoring weights: Heat Risk 40% · Solar Potential 30% · Public Impact 20% · Feasibility 10%")
    _card_close()


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    inject_css()

    try:
        df = load_data()
    except FileNotFoundError:
        st.error(f"Dataset not found: `{DATA_PATH}`. Run the data pipeline first.")
        st.stop()

    min_score = 0
    top_n = 20

    # ── HERO ──────────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="hero">'
        "<h1>🌱 SunShield AI — Your Campus Solar Planning Co-Pilot</h1>"
        '<p>"From weeks of analysis to minutes of clarity"</p>'
        "<small>By Prompt Pioneer &nbsp;|&nbsp; DataHacks 2026</small>"
        "</div>",
        unsafe_allow_html=True,
    )

    # ── 💰 BUDGET CONTROL ─────────────────────────────────────────────────────
    st.markdown(
        '<div class="budget-card">'
        '<div class="insight-label">💰 Set Your Planning Budget</div>'
        "</div>",
        unsafe_allow_html=True,
    )
    budget = st.slider(
        "",
        min_value=50_000,
        max_value=500_000,
        value=150_000,
        step=10_000,
        key="budget_slider",
        help="Adjust to see which sites fit within your budget",
        label_visibility="collapsed",
    )
    st.markdown(
        f'<div style="text-align:center;background:{CARD};border:1px solid {BORDER};'
        f"border-left:5px solid {GREEN};border-top:none;border-radius:0 0 16px 16px;"
        f'padding:8px 24px 18px;margin-top:-6px;box-shadow:0 2px 8px rgba(11,61,46,0.08);margin-bottom:16px;">'
        f'<span style="color:#000000;font-weight:800;font-size:2.8rem;">${budget:,}</span>'
        f'<p style="color:#888;font-size:0.82rem;margin:4px 0 0;">👆 Move slider to explore site recommendations</p>'
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── Filters + optimization ────────────────────────────────────────────────
    filtered = df.copy()
    selected = greedy_select(filtered, budget)
    selected_ids = set(selected["site_id"]) if not selected.empty else set()

    # ── 💡 KEY INSIGHTS ───────────────────────────────────────────────────────
    insight_key = f"{budget}"
    if st.session_state.get("_ikey") != insight_key:
        st.session_state["_itext"] = build_insight(selected, budget)
        st.session_state["_ikey"] = insight_key

    ins_col, btn_col = st.columns([5, 1])
    with ins_col:
        st.markdown(
            f'<div class="insight-box">'
            f'<div class="insight-label">💡 Key Insights — AI Generated</div>'
            f'<div class="insight-text">{st.session_state["_itext"]}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )
    with btn_col:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("🔄 Regenerate\nInsight", key="regen"):
            with st.spinner("Thinking..."):
                st.session_state["_itext"] = build_insight(selected, budget)

    # ── 📥 EXPORT ─────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="sec-title">📥 Export Your Results</div>', unsafe_allow_html=True
    )
    ex1, ex2, ex3, ex4 = st.columns(4)

    today = pd.Timestamp.now().strftime("%Y%m%d")

    with ex1:
        st.download_button(
            label="📊 All Sites (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=f"sunshield_all_sites_{today}.csv",
            mime="text/csv",
            use_container_width=True,
            help="All 25 candidate sites with scores",
        )

    with ex2:
        if not selected.empty:
            st.download_button(
                label="✅ Selected Sites (CSV)",
                data=selected.to_csv(index=False).encode("utf-8"),
                file_name=f"sunshield_selected_{today}.csv",
                mime="text/csv",
                use_container_width=True,
                help="Only budget-optimised sites",
            )
        else:
            st.button(
                "✅ Selected Sites (CSV)", disabled=True, use_container_width=True
            )

    with ex3:
        if not selected.empty:
            props_cols = [
                "name",
                "site_id",
                "dual_benefit_score",
                "heat_risk_score",
                "solar_potential_score",
                "public_impact_score",
                "feasibility_score",
                "installation_cost",
                "pedestrians_per_day",
                "estimated_kwh_per_year",
                "temp_delta",
                "site_type",
            ]
            features = [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(r.longitude), float(r.latitude)],
                    },
                    "properties": {
                        c: (
                            float(r[c])
                            if pd.api.types.is_float_dtype(selected[c])
                            else int(r[c])
                            if pd.api.types.is_integer_dtype(selected[c])
                            else str(r[c])
                        )
                        for c in props_cols
                    },
                }
                for _, r in selected.iterrows()
            ]
            geojson_str = json.dumps(
                {
                    "type": "FeatureCollection",
                    "name": "SunShield AI Recommendations",
                    "features": features,
                },
                indent=2,
            )
            st.download_button(
                label="🗺️ GeoJSON (GIS)",
                data=geojson_str,
                file_name=f"sunshield_sites_{today}.geojson",
                mime="application/geo+json",
                use_container_width=True,
                help="Import into ArcGIS, QGIS, or Google Earth",
            )
        else:
            st.button("🗺️ GeoJSON (GIS)", disabled=True, use_container_width=True)

    with ex4:
        st.markdown(
            f'<div style="background:{BORDER2};border:1px solid {BORDER};border-radius:12px;'
            f'padding:14px 16px;font-size:0.82rem;line-height:1.7;color:{TEXT};">'
            f'<div style="font-weight:700;color:{GREEN};margin-bottom:6px;">ℹ️ How to Use</div>'
            f'<b>CSV</b> — Excel, Google Sheets, any GIS tool<br>'
            f'<b>GeoJSON</b> — QGIS: <i>Add Layer → Vector</i><br>'
            f'ArcGIS: <i>Add Data → .geojson</i><br>'
            f'Google Earth: import as KML alternative<br><br>'
            f'All exports include coordinates and full scores.'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.caption("💡 Export data to integrate with your existing urban planning tools")

    # ── 📊 AT A GLANCE ────────────────────────────────────────────────────────
    n_sel = len(selected)
    spent = int(selected["installation_cost"].sum()) if not selected.empty else 0
    people = int(selected["pedestrians_per_day"].sum()) if not selected.empty else 0
    kwh = int(selected["estimated_kwh_per_year"].sum()) if not selected.empty else 0

    st.markdown(
        '<div class="kpi-row">'
        f'<div class="kpi-card"><div class="kpi-label">📍 Sites Selected</div>'
        f'<div class="kpi-value">{n_sel}</div><div class="kpi-sub">of {len(filtered)} candidates</div></div>'
        f'<div class="kpi-card"><div class="kpi-label">💰 Budget Spent</div>'
        f'<div class="kpi-value">${spent:,}</div><div class="kpi-sub">of ${budget:,}</div></div>'
        f'<div class="kpi-card"><div class="kpi-label">👥 People Protected</div>'
        f'<div class="kpi-value">{people:,}</div><div class="kpi-sub">daily foot traffic</div></div>'
        f'<div class="kpi-card"><div class="kpi-label">⚡ Clean Energy</div>'
        f'<div class="kpi-value">{kwh:,}</div><div class="kpi-sub">kWh / year</div></div>'
        "</div>",
        unsafe_allow_html=True,
    )

    # ── 🗺️ WHERE TO BUILD ─────────────────────────────────────────────────────
    st.markdown('<div class="sec-title">🗺️ Where to Build</div>', unsafe_allow_html=True)
    st.caption(
        "☀️ Selected sites  ·  Sage–green dots = other candidates (darker = higher score)  ·  Hover for details"
    )
    map_df = filtered.nlargest(top_n, "dual_benefit_score")
    st.plotly_chart(build_map(map_df, selected_ids), width="stretch")

    # ── 🌡️ CAMPUS HEAT MAP ────────────────────────────────────────────────────
    st.markdown(
        '<div class="sec-title">🌡️ Campus Temperature Heat Map</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Live sensor data from bike & walk traversals · Color = temperature °C · Hover for readings"
    )
    hdf = load_heatmap_data()
    if hdf.empty:
        st.info("No raw sensor files found. Place .txt files in `src/data/raw/`.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Readings", f"{len(hdf):,}")
        c2.metric(
            "Temp Range", f"{hdf['temp_c'].min():.1f}°C – {hdf['temp_c'].max():.1f}°C"
        )
        c3.metric("Avg Humidity", f"{hdf['rh'].mean():.0f}%")
        st.plotly_chart(build_heatmap(hdf), width="stretch")

    # ── ✅ RECOMMENDED SITES ──────────────────────────────────────────────────
    st.markdown(
        '<div class="sec-title">✅ Your Recommended Sites</div>', unsafe_allow_html=True
    )

    if selected.empty:
        st.warning(
            "No sites fit within the current budget. Try increasing the budget or adjusting filters."
        )
        st.stop()

    for rank, (_, row) in enumerate(selected.iterrows(), start=1):
        is_top = rank == 1
        top_badge = '<span class="top-badge">Top Pick</span>' if is_top else ""
        card_html = (
            f'<div class="site-card{"  top" if is_top else ""}">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">'
            f'<div>{top_badge}<span class="site-rank">#{rank}</span> <span class="site-name">{row["name"]}</span></div>'
            f'<span class="score-pill">Score: {row["dual_benefit_score"]:.1f} / 100</span>'
            f"</div>"
            f'<div class="why-label">💡 Why this site?</div>'
            + why_bullets_html(row)
            + "</div>"
        )
        st.markdown(card_html, unsafe_allow_html=True)

        grant_key = f"grant_{row['site_id']}"
        bd_key = f"bd_{row['site_id']}"

        b1, b2, _ = st.columns([1.6, 1.6, 3])
        with b1:
            btn_label = (
                "🤖 Regenerate Justification"
                if st.session_state.get(grant_key)
                else "🤖 Generate Grant Text"
            )
            if st.button(
                btn_label,
                key=f"btn_{grant_key}",
                use_container_width=True,
                type="primary" if is_top else "secondary",
            ):
                with st.spinner("Writing grant justification..."):
                    st.session_state[grant_key] = build_grant(row)
        with b2:
            lbl = (
                "📊 Hide Breakdown"
                if st.session_state.get(bd_key)
                else "📊 Show Score Breakdown"
            )
            if st.button(lbl, key=f"btn_{bd_key}", use_container_width=True):
                st.session_state[bd_key] = not st.session_state.get(bd_key, False)

        grant_txt = st.session_state.get(grant_key)
        if grant_txt:
            if is_top:
                st.markdown(
                    '<div class="insight-label" style="margin-top:12px;">📝 Grant Justification — Ready to Copy</div>',
                    unsafe_allow_html=True,
                )
                st.text_area(
                    "Copy into your grant proposal:",
                    value=grant_txt,
                    height=220,
                    key=f"ta_{grant_key}",
                    label_visibility="collapsed",
                )
                st.download_button(
                    label="📥 Download as .txt",
                    data=grant_txt,
                    file_name=f"grant_{row['site_id']}_{pd.Timestamp.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    key=f"dl_{grant_key}",
                )
                st.caption(
                    "💡 Edit this text to match your specific grant requirements"
                )
            else:
                st.info(f"📄 {grant_txt}")

        if st.session_state.get(f"bd_{row['site_id']}"):
            st.markdown(
                '<div class="breakdown-wrap">'
                + bar_html("Heat Risk", row["heat_risk_score"], "#E05C4A", "40%")
                + bar_html(
                    "Solar Potential", row["solar_potential_score"], "#D4A017", "30%"
                )
                + bar_html(
                    "Public Impact", row["public_impact_score"], "#4A90D9", "20%"
                )
                + bar_html("Feasibility", row["feasibility_score"], "#3A9E78", "10%")
                + "</div>",
                unsafe_allow_html=True,
            )

    # ── Collapsed sections ────────────────────────────────────────────────────
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    render_whatif(filtered, budget, selected)
    render_deepdive(selected)


if __name__ == "__main__":
    main()
st.markdown(
    """
<style>

/* ALL buttons */
div.stButton > button {
    background: #0f172a !important;   /* deep navy */
    color: white !important;
    border-radius: 12px !important;
    padding: 10px 20px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    font-weight: 500;
    transition: all 0.25s ease;
}

/* Hover */
div.stButton > button:hover {
    background: #1e293b !important;  /* lighter navy */
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.2);
}

/* Click */
div.stButton > button:active {
    transform: scale(0.98);
    box-shadow: none;
}

/* Fix light buttons like "How to Use" */
div.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #0f172a !important;
    border: 1px solid #0f172a !important;
}

/* Hover for secondary */
div.stButton > button[kind="secondary"]:hover {
    background: #0f172a !important;
    color: white !important;
}

</style>
""",
    unsafe_allow_html=True,
)
