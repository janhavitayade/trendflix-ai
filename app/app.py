import streamlit as st
import sqlite3
import pandas as pd
import base64
import os
import datetime

# --------------------------------------------------
# NEW: joblib is used to load the persisted Extra Trees model
# (see benchmark_models.py, which now saves models/extra_trees_model.pkl
# and models/feature_columns.pkl) so the Predict page can score
# user-entered inputs without retraining anything at runtime.
# --------------------------------------------------
import joblib

# --------------------------------------------------
# NEW: Plotly is used only to REPLACE the flat st.bar_chart() calls
# with dark, Netflix-themed charts. No data/query logic changes —
# same dataframes, same SQL, just a nicer renderer.
# Run: pip install plotly
# --------------------------------------------------
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# NEW: logo-as-base64 helper.
# WHY: st.image() renders inside Streamlit's own internal container
# (data-testid="stImage"), and that container's default CSS varies
# across Streamlit versions with a specificity that can beat our
# override — which is why centering it via CSS alone was unreliable.
# Instead, we read the PNG once and inline it as a base64 data URI
# inside a plain <div style="text-align:center">, which is just
# regular HTML/CSS with nothing Streamlit-specific to fight against.
# --------------------------------------------------

def get_base64_image(path):
    """Return a base64 data URI for a local image, or None if missing."""
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{encoded}"

# --------------------------------------------------
# NEW: cached loader for the production model.
# WHY cache_resource: joblib.load() opens a file and reconstructs a
# fitted sklearn estimator — that's relatively expensive to redo on
# every single widget interaction/rerun. st.cache_resource keeps the
# same in-memory model object across reruns until the underlying file
# changes or the process restarts.
# --------------------------------------------------

@st.cache_resource
def load_production_model():
    """Load the saved Extra Trees model + its expected feature order.

    Returns (model, feature_columns) or (None, None) if the artifacts
    haven't been generated yet (i.e. benchmark_models.py hasn't been
    run since the joblib.dump() lines were added to it).
    """
    model_path = "models/extra_trees_model.pkl"
    columns_path = "models/feature_columns.pkl"

    if not os.path.exists(model_path) or not os.path.exists(columns_path):
        return None, None

    model = joblib.load(model_path)
    feature_columns = joblib.load(columns_path)
    return model, feature_columns

# --------------------------------------------------
# PAGE CONFIG
# CHANGED: page_icon now points to the PNG favicon (assets/trendflix_favicon.png)
# instead of the 🎬 emoji. This is what shows up in the browser tab
# (Chrome/Edge) next to the page title.
#
# IMPORTANT: page_icon needs a raster image (PNG/JPG), a PIL Image,
# or an emoji — it does NOT reliably accept .svg. Streamlit's SVG
# support in st.image / page_icon has been flaky/version-dependent
# (see streamlit/streamlit#9098, #3882), so we rasterize the logo to
# PNG once (see assets/trendflix_logo.png) and use that everywhere.
# --------------------------------------------------

st.set_page_config(
    page_title="TrendFlix AI",
    page_icon="assets/trendflix_favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# NETFLIX-STYLE THEME (CSS INJECTION)
# NEW BLOCK: this is pure presentation. It does not touch any
# Streamlit widget logic, callbacks, or data flow — it only
# restyles how existing elements render (colors, fonts, spacing).
#
# Design tokens used throughout this file:
#   App background   : #141414  (Netflix black)
#   Card background  : #181818 / #1F1F1F
#   Accent (brand)   : #E50914  (Netflix red)
#   Text primary     : #F5F5F1
#   Text secondary   : #B3B3B3
#   Rating gold      : #F5C518
#   Display font     : 'Bebas Neue' (condensed, Netflix-like headline face)
#   Body font        : 'Inter'
# --------------------------------------------------

NETFLIX_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --nf-bg: #141414;
    --nf-card: #181818;
    --nf-card-alt: #1f1f1f;
    --nf-red: #e50914;
    --nf-red-dark: #b20710;
    --nf-text: #f5f5f1;
    --nf-text-dim: #b3b3b3;
    --nf-gold: #f5c518;
    --nf-border: #2a2a2a;
}

/* ---- App-wide background & base typography ---- */
.stApp {
    background: var(--nf-bg);
    color: var(--nf-text);
    font-family: 'Inter', sans-serif;
}

/* Hide default Streamlit chrome for a cleaner "product" feel */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {background: transparent !important;}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: #000000;
    border-right: 1px solid var(--nf-border);
}
[data-testid="stSidebar"] * {
    color: var(--nf-text) !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    padding: 6px 10px;
    border-radius: 4px;
    transition: background 0.2s ease;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: #1a1a1a;
}

/* ---- Headline / display type scale ---- */
.nf-hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 84px;
    letter-spacing: 2px;
    color: var(--nf-red);
    line-height: 1;
    margin-bottom: 0;
    text-shadow: 0 4px 24px rgba(229,9,20,0.35);
}
/* FIX: the hero markup below uses class="nf-hero-subtitle" — this
   rule previously existed only as ".nf-hero-sub", so the subtitle
   line was rendering as unstyled plain text. Renamed to match. */
.nf-hero-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 20px;
    font-weight: 500;
    color: var(--nf-text-dim);
    margin-top: 6px;
}
.nf-section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 34px;
    letter-spacing: 1px;
    color: var(--nf-text);
    margin-bottom: 4px;
}
.nf-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--nf-red);
    margin-bottom: 2px;
}

/* ---- Hero banner (Overview page) ---- */
.nf-hero-banner {
    background: linear-gradient(180deg, rgba(20,20,20,0) 0%, rgba(20,20,20,0.85) 75%, #141414 100%),
                radial-gradient(circle at 20% 20%, rgba(229,9,20,0.35) 0%, rgba(20,20,20,0) 55%),
                linear-gradient(120deg, #1a1a1a 0%, #0d0d0d 100%);
    border-radius: 10px;
    padding: 40px 48px 56px 48px;
    margin-bottom: 28px;
    border: 1px solid var(--nf-border);
}

/* ---- KPI tiles (replaces st.metric visuals) ---- */
.nf-kpi-card {
    background: var(--nf-card);
    border: 1px solid var(--nf-border);
    border-left: 4px solid var(--nf-red);
    border-radius: 6px;
    padding: 18px 20px;
    height: 100%;
}
.nf-kpi-label {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--nf-text-dim);
    margin-bottom: 6px;
}
.nf-kpi-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 40px;
    color: var(--nf-text);
    letter-spacing: 1px;
}

/* ---- Generic content card ---- */
.nf-card {
    background: var(--nf-card);
    border: 1px solid var(--nf-border);
    border-radius: 8px;
    padding: 22px 24px;
    margin-bottom: 18px;
}

/* ---- Top-10 style ranked row ---- */
.nf-rank-badge {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 46px;
    color: var(--nf-red);
    -webkit-text-stroke: 1px #7a0006;
    line-height: 1;
    min-width: 46px;
    text-align: center;
}
.nf-rank-name {
    font-weight: 600;
    font-size: 15px;
    color: var(--nf-text);
}
.nf-rank-rating {
    font-size: 13px;
    color: var(--nf-gold);
    font-weight: 700;
}

/* ---- Prediction result tile ---- */
.nf-predict-result {
    background: linear-gradient(120deg, #1a1a1a 0%, #0d0d0d 100%);
    border: 1px solid var(--nf-red);
    border-radius: 10px;
    padding: 28px 32px;
    text-align: center;
    margin-top: 10px;
}
.nf-predict-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 64px;
    color: var(--nf-red);
    letter-spacing: 1px;
    line-height: 1;
}
.nf-predict-label {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--nf-text-dim);
    margin-bottom: 8px;
}

/* NOTE: the hero logo no longer uses st.image() (see get_base64_image
   helper above) — it's inlined as base64 in a plain centered <div>,
   which sidesteps Streamlit's own image container styling entirely.
   No CSS override needed for it anymore. */

/* ---- Pipeline / architecture steps (now an animated flow) ---- */
.nf-pipe-step {
    background: var(--nf-card-alt);
    border: 1px solid var(--nf-border);
    border-radius: 6px;
    padding: 14px 10px;
    text-align: center;
    font-size: 12px;
    font-weight: 600;
    color: var(--nf-text);
    box-shadow: 0 0 0 rgba(229,9,20,0);
    transition: box-shadow 0.3s ease;
}
.nf-pipe-step:hover {
    box-shadow: 0 0 14px rgba(229,9,20,0.35);
    border-color: var(--nf-red);
}

/* Horizontal connector between two nodes in the same row: three
   chevrons animate in a staggered wave to read as "data moving
   left to right", instead of a single static arrow. */
.nf-flow-arrow {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    gap: 2px;
}
.nf-flow-arrow span {
    color: var(--nf-red);
    font-size: 18px;
    font-weight: 900;
    opacity: 0.25;
    animation: nf-flow-pulse 1.4s ease-in-out infinite;
}
.nf-flow-arrow span:nth-child(2) { animation-delay: 0.15s; }
.nf-flow-arrow span:nth-child(3) { animation-delay: 0.3s; }

@keyframes nf-flow-pulse {
    0%   { opacity: 0.2; transform: translateX(-2px); }
    50%  { opacity: 1;   transform: translateX(2px); }
    100% { opacity: 0.2; transform: translateX(-2px); }
}

/* Vertical connector bridging row 1 -> row 2: a single down-arrow
   that gently bounces, signaling "continue reading down". */
.nf-flow-arrow-down {
    text-align: center;
    font-size: 30px;
    line-height: 1;
    color: var(--nf-red);
    animation: nf-flow-bounce 1.3s ease-in-out infinite;
}

@keyframes nf-flow-bounce {
    0%, 100% { transform: translateY(0);  opacity: 0.45; }
    50%      { transform: translateY(8px); opacity: 1; }
}

/* Respect reduced-motion preferences */
@media (prefers-reduced-motion: reduce) {
    .nf-flow-arrow span, .nf-flow-arrow-down {
        animation: none !important;
        opacity: 0.9 !important;
    }
}

/* ---- Dataframe container polish ---- */
[data-testid="stDataFrame"] {
    border: 1px solid var(--nf-border);
    border-radius: 8px;
    overflow: hidden;
}

/* ---- Divider ---- */
hr {
    border-color: var(--nf-border) !important;
}

/* ---- Metric fallback (native st.metric, used sparingly) ---- */
[data-testid="stMetricValue"] {
    color: var(--nf-text) !important;
    font-family: 'Bebas Neue', sans-serif;
}
[data-testid="stMetricLabel"] {
    color: var(--nf-text-dim) !important;
}
</style>
"""

st.markdown(NETFLIX_CSS, unsafe_allow_html=True)

# --------------------------------------------------
# SHARED PLOTLY DARK TEMPLATE
# NEW: one reusable helper so every chart on the dashboard shares the
# same Netflix-dark look instead of Streamlit's default light chart style.
# --------------------------------------------------

def style_fig(fig, height=380):
    """Apply the shared Netflix-dark styling to any Plotly figure."""
    fig.update_layout(
        paper_bgcolor="#181818",
        plot_bgcolor="#181818",
        font=dict(family="Inter, sans-serif", color="#F5F5F1"),
        margin=dict(l=10, r=10, t=40, b=10),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(showgrid=False, color="#B3B3B3")
    fig.update_yaxes(showgrid=True, gridcolor="#2a2a2a", color="#B3B3B3")
    return fig

# --------------------------------------------------
# DATABASE CONNECTION
# UNCHANGED path/DB logic. Only added check_same_thread=False, which
# is a standard Streamlit-with-SQLite stability flag (Streamlit can
# touch the connection from different internal threads on rerun) —
# not a schema or query change.
# --------------------------------------------------

connection = sqlite3.connect("database/trendflix.db", check_same_thread=False)

# --------------------------------------------------
# LOAD DATA
# UNCHANGED — identical queries to the original file.
# --------------------------------------------------

shows_df = pd.read_sql_query(
    "SELECT * FROM shows",
    connection
)

avg_rating = pd.read_sql_query(
    """
    SELECT AVG(rating)
    FROM snapshots
    WHERE rating IS NOT NULL
    """,
    connection
).iloc[0, 0]

snapshot_count = pd.read_sql_query(
    """
    SELECT COUNT(*) AS total
    FROM snapshots
    """,
    connection
).iloc[0, 0]

# --------------------------------------------------
# KPI CALCULATIONS
# UNCHANGED
# --------------------------------------------------

total_shows = len(shows_df)

running_shows = len(
    shows_df[shows_df["status"] == "Running"]
)

ended_shows = len(
    shows_df[shows_df["status"] == "Ended"]
)

# --------------------------------------------------
# SIDEBAR
# No logo here on purpose — you asked for the mark to live on the
# main page only, plus the browser tab (via page_icon above). The
# sidebar stays text-only navigation.
# --------------------------------------------------

st.sidebar.markdown("<div class='nf-eyebrow' style='padding-left:2px;'>NAVIGATE</div>", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Analytics",
        "Machine Learning",
        "Predict",
        "Dataset Explorer"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown(
    """
    <div class="nf-card" style="padding:14px 16px;">
        <div class="nf-eyebrow">Live Snapshot</div>
        <div style="color:#B3B3B3; font-size:13px; line-height:1.6;">
            Data source: TVMaze API<br>
            Storage: SQLite<br>
            Best model: Extra Trees Regressor
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# OVERVIEW PAGE
# --------------------------------------------------

if page == "Overview":

    # CHANGED (again): dropped st.image() + columns([1,2,1]) entirely.
    # That approach only gets the logo APPROXIMATELY centered — it
    # depends on Streamlit's internal image container CSS, which
    # varies by version and can override our centering rule. Inlining
    # the PNG as base64 inside a plain <div style="text-align:center">
    # removes Streamlit's image wrapper from the equation completely,
    # so centering is guaranteed by plain HTML/CSS, not by fighting
    # Streamlit's own styles.
    logo_data_uri = get_base64_image("assets/trendflix_logo.png")

    if logo_data_uri:
        st.markdown(
            f"""
            <div style="text-align:center;">
                <img src="{logo_data_uri}" width="180" style="display:inline-block;">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Graceful fallback if the asset path is wrong, so the page
        # still renders instead of silently showing nothing.
        st.warning("Logo not found at assets/trendflix_logo.png — check the file path.")

    # NEW: full hero banner replacing the plain st.title/st.subheader.
    # Same copy/intent as the original title + subheader + info box,
    # just presented as a Netflix-style title card.
    st.markdown(
        """
        <div class="nf-hero-banner" style="text-align:center;">
            <div class="nf-hero-title">TRENDFLIX AI</div>
            <div class="nf-hero-subtitle">
                OTT Trend Intelligence Platform
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # CHANGED: KPI cards. Same four values as the original
    # st.metric() calls (total_shows, running_shows, ended_shows,
    # avg_rating) — just rendered as custom Netflix-style tiles with
    # a red accent rail instead of default Streamlit metrics.
    col1, col2, col3, col4 = st.columns(4)

    kpi_data = [
        ("TOTAL SHOWS", total_shows),
        ("RUNNING SHOWS", running_shows),
        ("ENDED SHOWS", ended_shows),
        ("AVERAGE RATING", round(avg_rating, 2)),
    ]

    for col, (label, value) in zip([col1, col2, col3, col4], kpi_data):
        with col:
            st.markdown(
                f"""
                <div class="nf-kpi-card">
                    <div class="nf-kpi-label">{label}</div>
                    <div class="nf-kpi-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='nf-section-title'>Project Summary</div>", unsafe_allow_html=True)

    # CHANGED: same fields as the original st.info() summary block,
    # now laid out as a two-column spec sheet card for scannability.
    st.markdown(
        f"""
        <div class="nf-card">
            <div style="display:flex; flex-wrap:wrap; gap:32px;">
                <div><div class="nf-eyebrow">Data Source</div><div>TVMaze API</div></div>
                <div><div class="nf-eyebrow">Database</div><div>SQLite</div></div>
                <div><div class="nf-eyebrow">Shows</div><div>{total_shows}</div></div>
                <div><div class="nf-eyebrow">Snapshots</div><div>{snapshot_count}</div></div>
                <div><div class="nf-eyebrow">Best Model</div><div>Extra Trees Regressor</div></div>
                <div><div class="nf-eyebrow">R² Score</div><div>0.26</div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='nf-section-title'>Project Architecture</div>",
        unsafe_allow_html=True
    )

    # CHANGED: same six pipeline stages as before (unchanged content/
    # order), but now rendered as a connected, animated flow instead
    # of two isolated rows with a static arrow. Each pair of adjacent
    # nodes in a row gets an animated chevron connector (data moving
    # left -> right), and a bouncing arrow bridges row 1 into row 2 —
    # so it reads as one continuous pipeline, which is easier for a
    # first-time viewer to follow than two disconnected blocks.
    #
    # Layout uses a 5-column ratio per row: node, connector, node,
    # connector, node — the connector columns are deliberately narrow
    # (ratio 0.5) so they read as "in-between" the boxes, not as their
    # own step.
    stages_row1 = ["TVMaze API", "CSV Snapshots", "SQLite Database"]
    stages_row2 = ["SQL Analytics", "Machine Learning", "Streamlit Dashboard"]

    CONNECTOR_HTML = "<div class='nf-flow-arrow'><span>›</span><span>›</span><span>›</span></div>"

    def render_flow_row(stages):
        cols = st.columns([2, 0.5, 2, 0.5, 2])
        with cols[0]:
            st.markdown(f"<div class='nf-pipe-step'>{stages[0]}</div>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(CONNECTOR_HTML, unsafe_allow_html=True)
        with cols[2]:
            st.markdown(f"<div class='nf-pipe-step'>{stages[1]}</div>", unsafe_allow_html=True)
        with cols[3]:
            st.markdown(CONNECTOR_HTML, unsafe_allow_html=True)
        with cols[4]:
            st.markdown(f"<div class='nf-pipe-step'>{stages[2]}</div>", unsafe_allow_html=True)

    render_flow_row(stages_row1)

    st.markdown("<div class='nf-flow-arrow-down'>⬇</div>", unsafe_allow_html=True)

    render_flow_row(stages_row2)

# --------------------------------------------------
# ANALYTICS PAGE
# --------------------------------------------------

elif page == "Analytics":

    st.markdown("<div class='nf-eyebrow'>DEEP DIVE</div>", unsafe_allow_html=True)
    st.markdown("<div class='nf-hero-title' style='font-size:52px;'>📊 Analytics</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # UNCHANGED filter logic
    status_filter = st.selectbox(
        "Filter by Status",
        [
            "All",
            "Running",
            "Ended",
            "To Be Determined"
        ]
    )

    if status_filter == "All":
        filtered_df = shows_df
    else:
        filtered_df = shows_df[
            shows_df["status"] == status_filter
        ]

    st.markdown("<div class='nf-section-title'>Filtered Shows</div>", unsafe_allow_html=True)

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    st.divider()

    st.markdown("<div class='nf-section-title'>⭐ Top 10 Highest Rated Shows</div>", unsafe_allow_html=True)

    # UNCHANGED query
    top_rated_df = pd.read_sql_query(
        """
        SELECT
            shows.name,
            snapshots.rating
        FROM shows
        JOIN snapshots
        ON shows.id = snapshots.show_id
        WHERE snapshots.rating IS NOT NULL
        ORDER BY snapshots.rating DESC
        LIMIT 10
        """,
        connection
    )

    # NEW: rendered as a Netflix "Top 10" ranked list (big numeral +
    # name + rating) instead of a plain dataframe, using the exact
    # same top_rated_df rows/order the query already returns.
    rank_cols = st.columns(2)
    for idx, row in top_rated_df.reset_index(drop=True).iterrows():
        target_col = rank_cols[0] if idx % 2 == 0 else rank_cols[1]
        with target_col:
            st.markdown(
                f"""
                <div class="nf-card" style="display:flex; align-items:center; gap:16px; padding:14px 18px; margin-bottom:10px;">
                    <div class="nf-rank-badge">{idx + 1}</div>
                    <div>
                        <div class="nf-rank-name">{row['name']}</div>
                        <div class="nf-rank-rating">★ {row['rating']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with st.expander("View as table"):
        st.dataframe(top_rated_df, use_container_width=True)

    st.divider()

    st.markdown("<div class='nf-section-title'>📺 Show Status Distribution</div>", unsafe_allow_html=True)

    # UNCHANGED query
    status_df = pd.read_sql_query(
        """
        SELECT
            status,
            COUNT(*) AS count
        FROM shows
        GROUP BY status
        """,
        connection
    )

    # CHANGED: st.bar_chart -> styled Plotly donut. Same status_df data.
    fig_status = px.pie(
        status_df, names="status", values="count", hole=0.55,
        color_discrete_sequence=["#E50914", "#B3B3B3", "#F5C518", "#5A5A5A"]
    )
    fig_status.update_traces(textfont_color="#F5F5F1")
    st.plotly_chart(style_fig(fig_status, height=340), use_container_width=True)

    st.divider()

    st.markdown("<div class='nf-section-title'>🌍 Language Distribution</div>", unsafe_allow_html=True)

    # UNCHANGED query
    language_df = pd.read_sql_query(
        """
        SELECT
            language,
            COUNT(*) AS count
        FROM shows
        GROUP BY language
        ORDER BY count DESC
        """,
        connection
    )

    # CHANGED: st.bar_chart -> horizontal Plotly bar in Netflix red.
    # Same language_df data, same ordering.
    fig_lang = px.bar(
        language_df, x="count", y="language", orientation="h",
        color_discrete_sequence=["#E50914"]
    )
    fig_lang.update_layout(yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(style_fig(fig_lang), use_container_width=True)

# --------------------------------------------------
# MACHINE LEARNING PAGE
# --------------------------------------------------

elif page == "Machine Learning":

    st.markdown("<div class='nf-eyebrow'>MODEL LAB</div>", unsafe_allow_html=True)
    st.markdown("<div class='nf-hero-title' style='font-size:52px;'>🤖 Machine Learning</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='nf-section-title' style='font-size:26px;'>🏆 Production Model</div>", unsafe_allow_html=True)

    # UNCHANGED copy, restyled as a card instead of st.success
    st.markdown(
        """
        <div class="nf-card" style="border-left:4px solid #E50914;">
        Extra Trees Regressor has been selected as the production model
        after benchmarking five machine learning algorithms.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        **Models Evaluated**

        - Linear Regression
        - Decision Tree Regressor
        - Random Forest Regressor
        - Gradient Boosting Regressor
        - Extra Trees Regressor
        """
    )

    # UNCHANGED metric values (MAE / MSE / R²), restyled KPI tiles
    col1, col2, col3 = st.columns(3)
    ml_metrics = [("MAE", "6.40"), ("MSE", "148.68"), ("R² SCORE", "0.26")]
    for col, (label, value) in zip([col1, col2, col3], ml_metrics):
        with col:
            st.markdown(
                f"""
                <div class="nf-kpi-card">
                    <div class="nf-kpi-label">{label}</div>
                    <div class="nf-kpi-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    st.markdown("<div class='nf-section-title' style='font-size:26px;'>Features Used</div>", unsafe_allow_html=True)

    # UNCHANGED feature list, laid out as chips instead of stacked bullets
    features = ["rating", "status_encoded", "premiered_year", "averageRuntime", "genre_count", "show_age"]
    chip_html = "".join(
        f"<span style='background:#222; border:1px solid #2a2a2a; color:#F5F5F1; "
        f"padding:6px 14px; border-radius:20px; margin:4px; display:inline-block; font-size:13px;'>{f}</span>"
        for f in features
    )
    st.markdown(f"<div>{chip_html}</div>", unsafe_allow_html=True)

    st.divider()

    st.markdown("<div class='nf-section-title' style='font-size:26px;'>Model Leaderboard</div>", unsafe_allow_html=True)

    # UNCHANGED dataframe values — identical numbers to the original file
    comparison_df = pd.DataFrame(
        {
            "Model": [
                "Extra Trees",
                "Random Forest",
                "Decision Tree",
                "Gradient Boosting",
                "Linear Regression"
            ],
            "MAE": [
                6.40,
                6.57,
                7.18,
                6.79,
                7.32
            ],
            "MSE": [
                148.68,
                150.97,
                160.23,
                167.24,
                178.16
            ],
            "R²": [
                0.26,
                0.25,
                0.21,
                0.17,
                0.12
            ]
        }
    )

    st.dataframe(
        comparison_df,
        use_container_width=True
    )

    st.markdown("<div class='nf-section-title' style='font-size:26px;'>📈 Model Performance Comparison</div>", unsafe_allow_html=True)

    chart_df = comparison_df[
        ["Model", "R²"]
    ].set_index("Model")

    # CHANGED: st.bar_chart -> Plotly bar, same chart_df values,
    # with the winning model (Extra Trees) highlighted in Netflix red.
    fig_compare = px.bar(
        chart_df.reset_index(), x="Model", y="R²",
        color=chart_df.reset_index()["Model"] == "Extra Trees",
        color_discrete_map={True: "#E50914", False: "#5A5A5A"}
    )
    fig_compare.update_layout(showlegend=False)
    st.plotly_chart(style_fig(fig_compare), use_container_width=True)

    st.divider()

    st.markdown("<div class='nf-section-title' style='font-size:26px;'>Feature Importance</div>", unsafe_allow_html=True)

    # UNCHANGED importance values
    importance_df = pd.DataFrame(
        {
            "Feature": [
                "rating",
                "averageRuntime",
                "premiered_year",
                "show_age",
                "genre_count",
                "status_encoded"
            ],
            "Importance": [
                52.5777,
                14.8818,
                10.6499,
                10.2377,
                8.4437,
                3.2093
            ]
        }
    )

    # CHANGED: st.bar_chart -> horizontal Plotly bar sorted descending,
    # same importance_df data.
    fig_importance = px.bar(
        importance_df.sort_values("Importance"),
        x="Importance", y="Feature", orientation="h",
        color_discrete_sequence=["#E50914"]
    )
    st.plotly_chart(style_fig(fig_importance), use_container_width=True)

    st.markdown(
        """
        <div class="nf-card" style="border-left:4px solid #F5C518;">
        <b>Key Insight:</b><br><br>
        Rating is the strongest predictor of popularity, contributing over
        52% of the model's decision-making.<br><br>
        Runtime, show age, and premiere year also influence popularity,
        while show status has minimal impact.
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# NEW: PREDICT PAGE
# --------------------------------------------------
# Lets a user enter unseen/hypothetical show attributes and get a
# live "weight" (popularity) prediction from the saved Extra Trees
# model. Model + feature order are loaded once via load_production_model()
# (cached with st.cache_resource above).
#
# status_encoded ASSUMPTION: sklearn's LabelEncoder assigns codes in
# alphabetical order of the unique string labels by default. Given the
# three statuses used elsewhere in this app (Running / Ended / To Be
# Determined), alphabetical order gives:
#   Ended = 0, Running = 1, To Be Determined = 2
# If your original preprocessing notebook used a different mapping
# (e.g. a manual dict, or OrdinalEncoder with a custom category order),
# update STATUS_ENCODING_MAP below to match it exactly — otherwise
# predictions will be systematically off for shows that aren't "Ended".
# --------------------------------------------------

elif page == "Predict":

    st.markdown("<div class='nf-eyebrow'>LIVE INFERENCE</div>", unsafe_allow_html=True)
    st.markdown("<div class='nf-hero-title' style='font-size:52px;'>🔮 Predict Popularity</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    model, feature_columns = load_production_model()

    if model is None:
        st.warning(
            "No saved model found at `models/extra_trees_model.pkl`. "
            "Run `python benchmark_models.py` locally first (it now also "
            "saves the trained model + feature order to the `models/` "
            "folder), then commit those two files so Streamlit Cloud can "
            "load them."
        )
    else:
        st.markdown(
            """
            <div class="nf-card">
            Enter attributes for a hypothetical or unseen show below.
            The saved <b>Extra Trees Regressor</b> will predict its
            popularity <b>weight</b> score.
            </div>
            """,
            unsafe_allow_html=True
        )

        # ---- Status encoding map (see assumption note above) ----
        STATUS_ENCODING_MAP = {
            "Ended": 0,
            "Running": 1,
            "To Be Determined": 2
        }

        current_year = datetime.date.today().year

        with st.form("predict_form"):

            col1, col2 = st.columns(2)

            with col1:
                rating = st.slider(
                    "Rating",
                    min_value=0.0,
                    max_value=10.0,
                    value=7.5,
                    step=0.1
                )

                status_label = st.selectbox(
                    "Status",
                    list(STATUS_ENCODING_MAP.keys())
                )

                premiered_year = st.number_input(
                    "Premiered Year",
                    min_value=1950,
                    max_value=current_year,
                    value=2018,
                    step=1
                )

            with col2:
                average_runtime = st.number_input(
                    "Average Runtime (minutes)",
                    min_value=1,
                    max_value=300,
                    value=45,
                    step=1
                )

                genre_count = st.number_input(
                    "Genre Count",
                    min_value=1,
                    max_value=10,
                    value=2,
                    step=1
                )

                # show_age is derived the same way it would have been
                # during feature engineering (current_year - premiere
                # year) rather than asked for independently, since the
                # two fields are not truly independent inputs. Shown
                # as a disabled field so the user can see, not edit, it.
                show_age = current_year - premiered_year
                st.number_input(
                    "Show Age (auto-calculated)",
                    value=show_age,
                    disabled=True
                )

            submitted = st.form_submit_button("Predict Weight")

        if submitted:

            status_encoded = STATUS_ENCODING_MAP[status_label]

            input_row = pd.DataFrame(
                [{
                    "rating": rating,
                    "status_encoded": status_encoded,
                    "premiered_year": premiered_year,
                    "averageRuntime": average_runtime,
                    "genre_count": genre_count,
                    "show_age": show_age
                }]
            )

            # Reorder columns to exactly match training-time order,
            # regardless of the dict order used to build input_row.
            input_row = input_row[feature_columns]

            prediction = model.predict(input_row)[0]

            st.markdown(
                f"""
                <div class="nf-predict-result">
                    <div class="nf-predict-label">Predicted Weight</div>
                    <div class="nf-predict-value">{prediction:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.expander("View input sent to the model"):
                st.dataframe(input_row, use_container_width=True)

# --------------------------------------------------
# DATASET EXPLORER PAGE
# --------------------------------------------------

elif page == "Dataset Explorer":

    st.markdown("<div class='nf-eyebrow'>RAW DATA</div>", unsafe_allow_html=True)
    st.markdown("<div class='nf-hero-title' style='font-size:52px;'>🗂 Dataset Explorer</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # UNCHANGED search logic
    search = st.text_input(
        "Search Show Name"
    )

    if search:

        filtered_df = shows_df[
            shows_df["name"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    else:
        filtered_df = shows_df

    st.markdown(
        f"<div class='nf-eyebrow'>Rows Found: {len(filtered_df)}</div>",
        unsafe_allow_html=True
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "TrendFlix AI | OTT Trend Intelligence Platform | Built by Janhavi Tayade"
)

# --------------------------------------------------
# CLOSE CONNECTION
# UNCHANGED
# --------------------------------------------------

connection.close()
