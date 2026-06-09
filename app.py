import os
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

import modules.instagram as ig_module

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="J.A.R.V.I.S. — PokiStock Command Centre",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global styles ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
      [data-testid="stAppViewContainer"] { background: #0d0d0d; }
      [data-testid="stHeader"]           { background: transparent; }

      .jarvis-card {
        background: #141414;
        border: 1px solid #1f1f1f;
        border-radius: 12px;
        padding: 20px 22px;
        margin-bottom: 16px;
      }
      .jarvis-card:hover { border-color: #3a3a3a; transition: border-color .2s; }

      .accent-firebase { border-top: 3px solid #FF6D00; }
      .accent-clarity  { border-top: 3px solid #00ADEF; }
      .accent-ig       { border-top: 3px solid #E1306C; }

      .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #f0f0f0;
        line-height: 1.1;
      }
      .metric-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: .08em;
        color: #666;
        margin-bottom: 4px;
      }
      .metric-delta-pos { color: #00C896; font-size: 0.82rem; }
      .metric-delta-neg { color: #FF4C60; font-size: 0.82rem; }
      .metric-delta-neu { color: #888;    font-size: 0.82rem; }

      .col-heading {
        font-size: 1rem;
        font-weight: 600;
        color: #e0e0e0;
        margin-bottom: 18px;
        padding-bottom: 10px;
        border-bottom: 1px solid #1f1f1f;
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .pill {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 99px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: .05em;
      }
      .pill-green  { background:#0a2e22; color:#00C896; }
      .pill-orange { background:#2e1a00; color:#FF6D00; }
      .pill-blue   { background:#001a2e; color:#00ADEF; }
      .pill-pink   { background:#2e0014; color:#E1306C; }
      .pill-purple { background:#1a1833; color:#635BFF; }
      .pill-grey   { background:#1f1f1f; color:#555;    }

      .pre-launch-banner {
        background: #111;
        border: 1px dashed #2a2a2a;
        border-radius: 12px;
        padding: 28px 22px;
        text-align: center;
        margin-bottom: 16px;
      }
      .pre-launch-banner p  { color: #444; font-size: 0.82rem; margin: 0; }
      .pre-launch-banner h3 { color: #635BFF; font-size: 1.1rem; margin: 0 0 6px; }

      .jarvis-header { text-align: center; padding: 28px 0 24px; }
      .jarvis-header h1 {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: .15em;
        background: linear-gradient(90deg, #FF6D00, #E1306C, #00ADEF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
      }
      .jarvis-header p {
        color: #555; font-size: 0.85rem; margin-top: 6px; letter-spacing: .06em;
      }
      hr.jarvis { border: none; border-top: 1px solid #1a1a1a; margin: 8px 0 20px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def card(css_class=""):
    return f'<div class="jarvis-card {css_class}">'

def metric_html(label, value, delta="", delta_type="neu"):
    display = f"{value:,}" if isinstance(value, int) else (
        f"{value}%" if isinstance(value, float) else (value or "—")
    )
    delta_html = (
        f'<span class="metric-delta-{delta_type}">{delta}</span>' if delta else ""
    )
    return (
        f'<div class="metric-label">{label}</div>'
        f'<div class="metric-value">{display} {delta_html}</div>'
    )

def pill(text, style="grey"):
    return f'<span class="pill pill-{style}">{text}</span>'

def col_heading(icon, title, subtitle=""):
    sub = (
        f'<span style="color:#555;font-size:.75rem;margin-left:auto">{subtitle}</span>'
        if subtitle else ""
    )
    return f'<div class="col-heading">{icon} {title}{sub}</div>'

# ── Firebase placeholder data (module coming next) ────────────────────────────

FIREBASE = {
    "new_users_today": ("—", "", "neu"),
    "new_users_week":  ("—", "", "neu"),
    "dau":             ("—", "", "neu"),
    "mau":             ("—", "", "neu"),
    "session_dur":     ("—", "", "neu"),
    "retention_d1":    ("—", "", "neu"),
    "crash_free":      ("—", "", "neu"),
    "active_devices":  ("—", "", "neu"),
}

# ── Clarity placeholder data (module coming next) ─────────────────────────────

CLARITY = {
    "total_sessions": ("—", "", "neu"),
    "pages_per_sess": ("—", "", "neu"),
    "scroll_depth":   ("—", "", "neu"),
    "bounce_rate":    ("—", "", "neu"),
    "dead_clicks":    ("—", "", "neu"),
    "rage_clicks":    ("—", "", "neu"),
}

# ── Live Instagram data ───────────────────────────────────────────────────────

_ig = ig_module.get_all()
_ig_live = ig_module.is_connected()

def _ig_val(key, suffix=""):
    v = _ig.get(key)
    if v is None:
        return "—", "", "neu"
    if isinstance(v, float):
        return f"{v}%", "", "neu"
    if isinstance(v, int):
        return f"{v:,}{suffix}", "", "neu"
    return str(v), "", "neu"

# ── Header ────────────────────────────────────────────────────────────────────

st.markdown(
    f"""
    <div class="jarvis-header">
      <h1>J.A.R.V.I.S.</h1>
      <p>Just A Rather Very Intelligent System &nbsp;·&nbsp; PokiStock Command Centre
         &nbsp;·&nbsp; {datetime.utcnow().strftime("%d %b %Y, %H:%M UTC")}</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('<hr class="jarvis">', unsafe_allow_html=True)

# ── 3-Column layout ───────────────────────────────────────────────────────────

col_firebase, col_clarity, col_ig = st.columns(3, gap="large")

# ─────────────────────────────────────────
# COLUMN 1 — App Analytics (Firebase)
# ─────────────────────────────────────────
with col_firebase:
    st.markdown(col_heading("🔥", "App Analytics", "Firebase"), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            card("accent-firebase") +
            metric_html("New Users Today", *FIREBASE["new_users_today"]) +
            "</div>", unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            card("accent-firebase") +
            metric_html("New Users (7d)", *FIREBASE["new_users_week"]) +
            "</div>", unsafe_allow_html=True,
        )

    c3, c4 = st.columns(2)
    with c3:
        st.markdown(
            card("accent-firebase") +
            metric_html("Daily Active Users", *FIREBASE["dau"]) +
            "</div>", unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            card("accent-firebase") +
            metric_html("Monthly Active Users", *FIREBASE["mau"]) +
            "</div>", unsafe_allow_html=True,
        )

    c5, c6 = st.columns(2)
    with c5:
        st.markdown(
            card("accent-firebase") +
            metric_html("Avg Session", *FIREBASE["session_dur"]) +
            "</div>", unsafe_allow_html=True,
        )
    with c6:
        st.markdown(
            card("accent-firebase") +
            metric_html("D1 Retention", *FIREBASE["retention_d1"]) +
            "</div>", unsafe_allow_html=True,
        )

    c7, c8 = st.columns(2)
    with c7:
        st.markdown(
            card("accent-firebase") +
            metric_html("Crash-Free", *FIREBASE["crash_free"]) +
            "</div>", unsafe_allow_html=True,
        )
    with c8:
        st.markdown(
            card("accent-firebase") +
            metric_html("Active Devices", *FIREBASE["active_devices"]) +
            "</div>", unsafe_allow_html=True,
        )

    st.markdown(
        card("accent-firebase") +
        '<div class="metric-label">Firebase Status</div>' +
        pill("Not connected", "orange") + "&nbsp;" +
        pill("Module coming next", "grey") +
        "</div>", unsafe_allow_html=True,
    )

# ─────────────────────────────────────────
# COLUMN 2 — Website Analytics (Clarity)
# ─────────────────────────────────────────
with col_clarity:
    st.markdown(col_heading("🌐", "Website Analytics", "Microsoft Clarity"), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            card("accent-clarity") +
            metric_html("Total Sessions", *CLARITY["total_sessions"]) +
            "</div>", unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            card("accent-clarity") +
            metric_html("Pages / Session", *CLARITY["pages_per_sess"]) +
            "</div>", unsafe_allow_html=True,
        )

    c3, c4 = st.columns(2)
    with c3:
        st.markdown(
            card("accent-clarity") +
            metric_html("Avg Scroll Depth", *CLARITY["scroll_depth"]) +
            "</div>", unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            card("accent-clarity") +
            metric_html("Bounce Rate", *CLARITY["bounce_rate"]) +
            "</div>", unsafe_allow_html=True,
        )

    st.markdown(
        card("accent-clarity") +
        '<div class="metric-label" style="margin-bottom:12px">UX Friction Signals</div>' +
        metric_html("Dead Clicks", *CLARITY["dead_clicks"]) +
        "<br>" +
        metric_html("Rage Clicks", *CLARITY["rage_clicks"]) +
        "</div>", unsafe_allow_html=True,
    )

    st.markdown(
        card("accent-clarity") +
        '<div class="metric-label">Clarity Status</div>' +
        pill("Not connected", "blue") + "&nbsp;" +
        pill("Module coming next", "grey") +
        "</div>", unsafe_allow_html=True,
    )

# ─────────────────────────────────────────
# COLUMN 3 — Marketing (Instagram)
# ─────────────────────────────────────────
with col_ig:
    st.markdown(col_heading("📱", "Marketing", "Instagram"), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            card("accent-ig") +
            metric_html("Followers", *_ig_val("followers")) +
            "</div>", unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            card("accent-ig") +
            metric_html("Posts", *_ig_val("posts")) +
            "</div>", unsafe_allow_html=True,
        )

    c3, c4 = st.columns(2)
    with c3:
        st.markdown(
            card("accent-ig") +
            metric_html("Reach (7d)", *_ig_val("reach_week")) +
            "</div>", unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            card("accent-ig") +
            metric_html("Impressions (7d)", *_ig_val("impressions_week")) +
            "</div>", unsafe_allow_html=True,
        )

    c5, c6 = st.columns(2)
    with c5:
        st.markdown(
            card("accent-ig") +
            metric_html("Engagement Rate", *_ig_val("engagement_rate")) +
            "</div>", unsafe_allow_html=True,
        )
    with c6:
        st.markdown(
            card("accent-ig") +
            metric_html("Profile Visits (7d)", *_ig_val("profile_visits")) +
            "</div>", unsafe_allow_html=True,
        )

    ig_status_pill = pill("Live ✓", "green") if _ig_live else pill("Not connected", "pink")
    st.markdown(
        card("accent-ig") +
        '<div class="metric-label">Instagram Status</div>' +
        ig_status_pill + "&nbsp;" +
        pill("Instagram Graph API v20", "grey") +
        "</div>", unsafe_allow_html=True,
    )

    # Pre-launch Stripe placeholder
    st.markdown(
        '<div class="pre-launch-banner">'
        '<h3>💳 Stripe — Pre-launch</h3>'
        '<p>Revenue metrics will appear here once<br>monetisation is activated.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

# ── Footer ────────────────────────────────────────────────────────────────────

st.markdown('<hr class="jarvis">', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;color:#333;font-size:.75rem;letter-spacing:.05em">'
    "J.A.R.V.I.S. v0.3.0 &nbsp;·&nbsp; "
    "Instagram live · Firebase &amp; Clarity coming next"
    "</p>",
    unsafe_allow_html=True,
)
