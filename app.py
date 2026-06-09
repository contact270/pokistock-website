import streamlit as st
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
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
      /* Dark base */
      [data-testid="stAppViewContainer"] { background: #0d0d0d; }
      [data-testid="stHeader"]           { background: transparent; }

      /* Card wrapper */
      .jarvis-card {
        background: #141414;
        border: 1px solid #1f1f1f;
        border-radius: 12px;
        padding: 20px 22px;
        margin-bottom: 16px;
      }
      .jarvis-card:hover { border-color: #3a3a3a; transition: border-color .2s; }

      /* Column accent bars */
      .accent-firebase { border-top: 3px solid #FF6D00; }
      .accent-stripe   { border-top: 3px solid #635BFF; }
      .accent-webdev   { border-top: 3px solid #00C896; }

      /* Metric typography */
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

      /* Section heading */
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

      /* Status pill */
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
      .pill-purple { background:#1a1833; color:#635BFF; }
      .pill-red    { background:#2e0a0a; color:#FF4C60; }
      .pill-grey   { background:#1f1f1f; color:#888; }

      /* Master header */
      .jarvis-header {
        text-align: center;
        padding: 28px 0 24px;
      }
      .jarvis-header h1 {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: .15em;
        background: linear-gradient(90deg, #FF6D00, #635BFF, #00C896);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
      }
      .jarvis-header p {
        color: #555;
        font-size: 0.85rem;
        margin-top: 6px;
        letter-spacing: .06em;
      }

      /* Divider */
      hr.jarvis { border: none; border-top: 1px solid #1a1a1a; margin: 8px 0 20px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def card(css_class: str = "", key: str = ""):
    """Return an HTML card open tag with optional accent class."""
    return f'<div class="jarvis-card {css_class}">'

def metric_html(label: str, value: str, delta: str = "", delta_type: str = "neu") -> str:
    delta_class = f"metric-delta-{delta_type}"
    delta_html  = f'<span class="{delta_class}">{delta}</span>' if delta else ""
    return (
        f'<div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value} {delta_html}</div>'
    )

def pill(text: str, style: str = "grey") -> str:
    return f'<span class="pill pill-{style}">{text}</span>'

def col_heading(icon: str, title: str, subtitle: str = "") -> str:
    sub = f'<span style="color:#555;font-size:.75rem;margin-left:auto">{subtitle}</span>' if subtitle else ""
    return f'<div class="col-heading">{icon} {title}{sub}</div>'

# ── Placeholder data (swap for live API calls per module) ─────────────────────

FIREBASE_DATA = {
    "dau":             ("8,241",  "+12% vs last week",  "pos"),
    "mau":             ("61,034", "+5.2% vs last month", "pos"),
    "session_dur":     ("3m 42s", "−8s vs last week",   "neg"),
    "retention_d1":    ("42%",    "+3pp",                "pos"),
    "crash_free":      ("99.2%",  "−0.1pp",              "neg"),
    "active_devices":  ("12,490", "",                    "neu"),
}

STRIPE_DATA = {
    "mrr":             ("£4,820",  "+£340 MoM",   "pos"),
    "arr":             ("£57,840", "",             "neu"),
    "new_subs":        ("83",      "+11 vs prev",  "pos"),
    "churn":           ("2.4%",    "−0.3pp",       "pos"),
    "ltv":             ("£148",    "",             "neu"),
    "pending_payouts": ("£1,204",  "",             "neu"),
}

CLARITY_GITHUB_DATA = {
    "dead_clicks":     ("3.1%",   "−0.4pp",        "pos"),
    "rage_clicks":     ("0.8%",   "+0.2pp",         "neg"),
    "scroll_depth":    ("68%",    "+5pp",            "pos"),
    "open_issues":     ("14",     "+2 today",        "neg"),
    "open_prs":        ("3",      "",                "neu"),
    "ci_pass_rate":    ("94%",    "−2pp",            "neg"),
}

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

col_firebase, col_stripe, col_webdev = st.columns(3, gap="large")

# ────────────────────────────────────
# COLUMN 1 — App Performance (Firebase)
# ────────────────────────────────────
with col_firebase:
    st.markdown(col_heading("🔥", "App Performance", "Firebase"), unsafe_allow_html=True)

    # DAU / MAU
    st.markdown(
        card("accent-firebase") +
        metric_html("Daily Active Users", *FIREBASE_DATA["dau"]) +
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        card("accent-firebase") +
        metric_html("Monthly Active Users", *FIREBASE_DATA["mau"]) +
        "</div>",
        unsafe_allow_html=True,
    )

    # Session & Retention side-by-side
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            card("accent-firebase") +
            metric_html("Avg Session", *FIREBASE_DATA["session_dur"]) +
            "</div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            card("accent-firebase") +
            metric_html("D1 Retention", *FIREBASE_DATA["retention_d1"]) +
            "</div>",
            unsafe_allow_html=True,
        )

    # Crash-free / Active devices
    c3, c4 = st.columns(2)
    with c3:
        st.markdown(
            card("accent-firebase") +
            metric_html("Crash-Free", *FIREBASE_DATA["crash_free"]) +
            "</div>",
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            card("accent-firebase") +
            metric_html("Active Devices", *FIREBASE_DATA["active_devices"]) +
            "</div>",
            unsafe_allow_html=True,
        )

    # Status banner
    st.markdown(
        card("accent-firebase") +
        '<div class="metric-label">Service Health</div>' +
        pill("Firestore OK", "green") + "&nbsp;" +
        pill("Auth OK", "green") + "&nbsp;" +
        pill("Storage OK", "green") +
        "</div>",
        unsafe_allow_html=True,
    )

# ────────────────────────────────────
# COLUMN 2 — Financials (Stripe)
# ────────────────────────────────────
with col_stripe:
    st.markdown(col_heading("💳", "Financials", "Stripe"), unsafe_allow_html=True)

    # MRR
    st.markdown(
        card("accent-stripe") +
        metric_html("Monthly Recurring Revenue", *STRIPE_DATA["mrr"]) +
        "</div>",
        unsafe_allow_html=True,
    )

    # ARR
    st.markdown(
        card("accent-stripe") +
        metric_html("Annual Run Rate", *STRIPE_DATA["arr"]) +
        "</div>",
        unsafe_allow_html=True,
    )

    # New subs / Churn
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            card("accent-stripe") +
            metric_html("New Subs", *STRIPE_DATA["new_subs"]) +
            "</div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            card("accent-stripe") +
            metric_html("Churn Rate", *STRIPE_DATA["churn"]) +
            "</div>",
            unsafe_allow_html=True,
        )

    # LTV / Pending
    c3, c4 = st.columns(2)
    with c3:
        st.markdown(
            card("accent-stripe") +
            metric_html("Avg LTV", *STRIPE_DATA["ltv"]) +
            "</div>",
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            card("accent-stripe") +
            metric_html("Pending Payout", *STRIPE_DATA["pending_payouts"]) +
            "</div>",
            unsafe_allow_html=True,
        )

    # Payment status
    st.markdown(
        card("accent-stripe") +
        '<div class="metric-label">Payment Gateway</div>' +
        pill("Live Mode", "purple") + "&nbsp;" +
        pill("Webhooks OK", "green") + "&nbsp;" +
        pill("No Disputes", "green") +
        "</div>",
        unsafe_allow_html=True,
    )

# ────────────────────────────────────
# COLUMN 3 — Web / Dev (Clarity + GitHub)
# ────────────────────────────────────
with col_webdev:
    st.markdown(col_heading("🌐", "Web / Dev", "Clarity · GitHub"), unsafe_allow_html=True)

    # Clarity UX signals
    st.markdown(
        card("accent-webdev") +
        '<div class="metric-label" style="margin-bottom:12px">UX Signals — Microsoft Clarity</div>' +
        metric_html("Dead Clicks", *CLARITY_GITHUB_DATA["dead_clicks"]) +
        "<br>" +
        metric_html("Rage Clicks", *CLARITY_GITHUB_DATA["rage_clicks"]) +
        "<br>" +
        metric_html("Avg Scroll Depth", *CLARITY_GITHUB_DATA["scroll_depth"]) +
        "</div>",
        unsafe_allow_html=True,
    )

    # GitHub health
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            card("accent-webdev") +
            metric_html("Open Issues", *CLARITY_GITHUB_DATA["open_issues"]) +
            "</div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            card("accent-webdev") +
            metric_html("Open PRs", *CLARITY_GITHUB_DATA["open_prs"]) +
            "</div>",
            unsafe_allow_html=True,
        )

    # CI pass rate
    st.markdown(
        card("accent-webdev") +
        metric_html("CI Pass Rate", *CLARITY_GITHUB_DATA["ci_pass_rate"]) +
        "</div>",
        unsafe_allow_html=True,
    )

    # Repo status
    st.markdown(
        card("accent-webdev") +
        '<div class="metric-label">Repository Status</div>' +
        pill("main ✓ protected", "green") + "&nbsp;" +
        pill("3 open PRs", "orange") + "&nbsp;" +
        pill("CI passing", "green") +
        "</div>",
        unsafe_allow_html=True,
    )

# ── Footer ────────────────────────────────────────────────────────────────────

st.markdown('<hr class="jarvis">', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;color:#333;font-size:.75rem;letter-spacing:.05em">'
    "J.A.R.V.I.S. v0.1.0 &nbsp;·&nbsp; All metrics are placeholder data — "
    "connect live API keys to activate each module"
    "</p>",
    unsafe_allow_html=True,
)
