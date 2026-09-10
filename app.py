import streamlit as st
from PIL import Image

from src.config import (
    APP_SUBTITLE,
    APP_TITLE,
    SUPPORTED_IMAGE_TYPES,
    validate_project_files,
)
from src.detector import SafeVisionDetector
from src.utils import (
    format_percentage,
    get_detection_summary,
    get_safety_status,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SafeVision AI",
    page_icon="🦺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL PORTFOLIO UI
# ============================================================

st.markdown(
    """
    <style>
    /* ========================================================
       SAFE VISION AI — PREMIUM DARK DASHBOARD
       ======================================================== */

    :root {
        --bg: #f4f7fb;
        --panel: #ffffff;
        --panel-2: #f8fafc;
        --panel-3: #eef3f8;
        --border: #dbe3ed;
        --text: #172033;
        --muted: #64748b;
        --orange: #f97316;
        --orange-soft: #fb923c;
        --cyan: #089bd3;
        --green: #16a34a;
        --yellow: #d97706;
        --red: #dc2626;
    }

    .stApp {
        background:
            radial-gradient(circle at 75% 0%, rgba(37,189,243,.075), transparent 28%),
            radial-gradient(circle at 15% 5%, rgba(255,122,26,.06), transparent 24%),
            var(--bg);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(255,255,255,.92);
    }

    [data-testid="stAppViewContainer"] {
        background: transparent;
    }

    .block-container {
        max-width: 1500px;
        padding: 2.2rem 3rem 4rem 3rem;
    }

    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #0e1524 0%, #0a101d 100%);
        border-right: 1px solid #dce4ee;
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.5rem 1.15rem;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 11px;
        padding: 8px 4px 18px;
    }

    .sidebar-logo {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 11px;
        background: linear-gradient(135deg, #ff7a1a, #ff9b52);
        box-shadow: 0 8px 24px rgba(249,115,22,.20);
        font-size: 22px;
    }

    .sidebar-brand-title {
        color: #172033;
        font-size: 1.02rem;
        font-weight: 800;
        letter-spacing: -.3px;
    }

    .sidebar-brand-sub {
        color: #64748b;
        font-size: .68rem;
        margin-top: 2px;
    }

    .sidebar-section-title {
        color: #334155;
        font-size: .76rem;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin: 1.4rem 0 .7rem;
    }

    .class-row {
        display: flex;
        align-items: center;
        gap: 9px;
        padding: 6px 8px;
        margin: 2px 0;
        border-radius: 8px;
        color: #52647d;
        font-size: .82rem;
        transition: .2s ease;
    }

    .class-row:hover {
        background: #eef3f8;
        color: #172033;
    }

    .class-icon {
        width: 22px;
        text-align: center;
    }

    .tech-chip {
        display: inline-block;
        padding: 5px 8px;
        margin: 3px 3px 3px 0;
        border: 1px solid #d9e2ec;
        background: #f1f5f9;
        color: #64748b;
        border-radius: 7px;
        font-size: .7rem;
    }

    .sidebar-divider {
        height: 1px;
        background: #1e2a40;
        margin: 1.2rem 0;
    }

    .sidebar-footer {
        color: #718096;
        font-size: .66rem;
        line-height: 1.55;
        margin-top: 1.5rem;
    }

    /* ---------- Hero ---------- */

    .hero-wrap {
        position: relative;
        overflow: hidden;
        padding: 1.7rem 0 1.9rem;
    }

    .hero-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 5px 10px;
        border: 1px solid rgba(37,189,243,.22);
        background: rgba(37,189,243,.055);
        color: #7ddcff;
        border-radius: 999px;
        font-size: .68rem;
        font-weight: 800;
        letter-spacing: .1em;
        text-transform: uppercase;
        margin-bottom: .85rem;
    }

    .hero-title {
        margin: 0;
        font-size: clamp(2.6rem, 5vw, 4.2rem);
        line-height: .98;
        font-weight: 900;
        letter-spacing: -2.8px;
        color: #172033;
    }

    .hero-title .accent {
        color: var(--cyan);
    }

    .hero-subtitle {
        margin-top: .8rem;
        color: #334155;
        font-size: 1.05rem;
        font-weight: 600;
    }

    .hero-description {
        max-width: 940px;
        margin-top: .7rem;
        color: #64748b;
        font-size: .88rem;
        line-height: 1.75;
    }

    .hero-tech {
        margin-top: 1rem;
        color: #64748b;
        font-size: .72rem;
        letter-spacing: .03em;
    }

    /* ---------- General sections ---------- */

    .section-head {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 1.7rem 0 .85rem;
    }

    .section-icon {
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
        background: #edf3f8;
        border: 1px solid #d7e1ec;
        font-size: 15px;
    }

    .section-title {
        color: #f2f5f9;
        font-size: 1.02rem;
        font-weight: 800;
        letter-spacing: -.2px;
    }

    .section-caption {
        color: #64748b;
        font-size: .7rem;
        margin-left: auto;
    }

    /* ---------- Upload ---------- */

    [data-testid="stFileUploader"] {
        background: linear-gradient(145deg, #0e1728, #0a1120);
        border: 1px dashed #2b3b56;
        border-radius: 15px;
        padding: 7px;
        transition: .2s ease;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #089bd3;
    }

    [data-testid="stFileUploader"] section {
        background: transparent;
        border: none;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: transparent !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #64748b;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] svg {
        fill: var(--cyan);
    }

    /* ---------- Image cards ---------- */

    .image-card-title {
        color: #52647d;
        font-size: .72rem;
        font-weight: 800;
        letter-spacing: .07em;
        text-transform: uppercase;
        margin: 0 0 .5rem .15rem;
    }

    [data-testid="stImage"] {
        border-radius: 13px;
        overflow: hidden;
        border: 1px solid #dbe3ed;
        background: #ffffff;
    }

    /* ---------- Metric cards ---------- */

    .metric-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-top: .4rem;
    }

    .metric-card {
        position: relative;
        overflow: hidden;
        min-height: 126px;
        padding: 1.05rem 1.15rem;
        border: 1px solid #d9e2ec;
        border-radius: 14px;
        background:
            linear-gradient(145deg, rgba(18,29,49,.96), rgba(10,17,30,.98));
        box-shadow: 0 10px 28px rgba(30,55,90,.08);
    }

    .metric-card::after {
        content: "";
        position: absolute;
        right: -30px;
        top: -35px;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: rgba(8,155,211,.06);
    }

    .metric-label {
        color: #64748b;
        font-size: .64rem;
        font-weight: 800;
        letter-spacing: .1em;
    }

    .metric-value {
        color: #172033;
        font-size: 2rem;
        line-height: 1.1;
        font-weight: 900;
        margin-top: .45rem;
        letter-spacing: -1px;
    }

    .metric-hint {
        color: #718096;
        font-size: .68rem;
        margin-top: .35rem;
    }

    /* ---------- Status ---------- */

    .status-box {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 12px;
        padding: 11px 14px;
        border-radius: 10px;
        border: 1px solid #b8e0c8;
        background: #effaf2;
        color: #15803d;
        font-size: .78rem;
        font-weight: 700;
    }

    .status-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: var(--green);
        box-shadow: 0 0 14px rgba(34,197,94,.55);
    }

    .status-attention {
        border-color: #f1d39b;
        background: #fff8e8;
        color: #b45309;
    }

    .status-attention .status-dot {
        background: var(--yellow);
        box-shadow: 0 0 14px rgba(245,158,11,.5);
    }

    .status-danger {
        border-color: #f0c3c7;
        background: #fff3f3;
        color: #b91c1c;
    }

    .status-danger .status-dot {
        background: var(--red);
        box-shadow: 0 0 14px rgba(239,68,68,.5);
    }

    /* ---------- Compliance ---------- */

    .compliance-card {
        padding: .95rem 1rem;
        border: 1px solid #d9e2ec;
        border-radius: 12px;
        background: #ffffff;
    }

    .compliance-name {
        color: #8795aa;
        font-size: .69rem;
        font-weight: 700;
        margin-bottom: .4rem;
        text-transform: uppercase;
        letter-spacing: .04em;
    }

    .compliance-value {
        color: #f4f7fb;
        font-size: 1.45rem;
        font-weight: 900;
    }

    .progress-track {
        height: 5px;
        margin-top: .6rem;
        background: #dbe4ee;
        border-radius: 999px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #089bd3, #38bdf8);
    }

    /* ---------- Violation ---------- */

    .violation-card {
        padding: 12px 14px;
        margin: 7px 0;
        border-radius: 10px;
        border: 1px solid #5b282d;
        background: rgba(239,68,68,.055);
    }

    .violation-title {
        color: #ffb1b1;
        font-size: .8rem;
        font-weight: 800;
    }

    .violation-meta {
        color: #8e6b70;
        font-size: .68rem;
        margin-top: 3px;
    }

    .safe-box {
        padding: 12px 14px;
        border-radius: 10px;
        border: 1px solid #174a36;
        background: rgba(34,197,94,.05);
        color: #72d89b;
        font-size: .76rem;
    }

    /* ---------- Detection pills ---------- */

    .pill-wrap {
        display: flex;
        flex-wrap: wrap;
        gap: 7px;
    }

    .detection-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 10px;
        border-radius: 999px;
        background: #f1f5f9;
        border: 1px solid #d6e0eb;
        color: #475569;
        font-size: .69rem;
        font-weight: 700;
    }

    .pill-count {
        color: #0788bd;
        font-weight: 900;
    }

    /* ---------- Info ---------- */

    .info-box {
        padding: 13px 15px;
        border-radius: 11px;
        border: 1px solid #d9e2ec;
        background: #f8fafc;
        color: #5b6b82;
        font-size: .73rem;
        line-height: 1.7;
    }

    .info-box strong {
        color: #334155;
    }

    /* ---------- Expander ---------- */

    [data-testid="stExpander"] {
        border: 1px solid #d9e2ec !important;
        border-radius: 11px !important;
        background: #ffffff !important;
    }

    [data-testid="stExpander"] summary {
        color: #475569 !important;
        font-size: .78rem !important;
    }

    /* ---------- Streamlit native elements ---------- */

    .stAlert {
        border-radius: 10px !important;
    }

    .stMetric {
        background: transparent;
    }

    /* ---------- Footer ---------- */

    .footer {
        margin-top: 3.2rem;
        padding: 1.5rem 0 .3rem;
        border-top: 1px solid #dce4ee;
        text-align: center;
        color: #718096;
        font-size: .66rem;
        line-height: 1.8;
    }

    .footer strong {
        color: #52647d;
    }

    /* ---------- Responsive ---------- */

    @media (max-width: 900px) {
        .block-container {
            padding: 1.2rem 1rem 3rem;
        }

        .metric-grid {
            grid-template-columns: 1fr;
        }

        .hero-title {
            font-size: 2.7rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# ============================================================
# FINAL HIGH-CONTRAST OVERRIDES
# ============================================================

st.markdown(
    """
    <style>
    /* ========================================================
       HIGH CONTRAST / READABILITY PASS
       ======================================================== */

    /* Main application */
    .stApp {
        background: #f5f7fb !important;
        color: #172033 !important;
    }

    .block-container {
        color: #172033 !important;
    }

    /* Hero */
    .hero-title,
    .hero-title .accent {
        color: #172033 !important;
    }

    .hero-title .accent {
        color: #0788bd !important;
    }

    .hero-subtitle {
        color: #26364d !important;
    }

    .hero-description {
        color: #475569 !important;
    }

    .hero-tech {
        color: #52647d !important;
    }

    .hero-eyebrow {
        color: #087aa9 !important;
        background: #edf9fd !important;
        border-color: #a9dff0 !important;
    }

    /* Section headings */
    .section-title {
        color: #172033 !important;
    }

    .section-caption {
        color: #52647d !important;
        font-weight: 700 !important;
    }

    .section-icon {
        background: #eef3f8 !important;
        border-color: #cbd7e4 !important;
    }

    /* Upload area */
    [data-testid="stFileUploader"] {
        background: #ffffff !important;
        border-color: #9fb3c8 !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        color: #334155 !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #475569 !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] small {
        color: #64748b !important;
    }

    /* Uploaded file name */
    [data-testid="stFileUploaderFileName"] {
        color: #172033 !important;
        font-weight: 700 !important;
    }

    /* Image labels */
    .image-card-title {
        color: #3f5068 !important;
    }

    /* KPI cards */
    .metric-card {
        background: #ffffff !important;
        border-color: #ccd8e5 !important;
        box-shadow: 0 8px 24px rgba(31, 55, 85, 0.08) !important;
    }

    .metric-label {
        color: #52647d !important;
    }

    .metric-value {
        color: #172033 !important;
    }

    .metric-hint {
        color: #64748b !important;
    }

    /* Safety status */
    .status-box {
        color: #166534 !important;
        background: #effaf3 !important;
        border-color: #a8dfbd !important;
    }

    .status-box strong {
        color: #14532d !important;
    }

    .status-attention {
        color: #92400e !important;
        background: #fff8e8 !important;
        border-color: #f0d39b !important;
    }

    .status-danger {
        color: #991b1b !important;
        background: #fff3f3 !important;
        border-color: #efb7bb !important;
    }

    /* PPE compliance */
    .compliance-card {
        background: #ffffff !important;
        border-color: #ccd8e5 !important;
    }

    .compliance-name {
        color: #52647d !important;
    }

    .compliance-value {
        color: #172033 !important;
    }

    .progress-track {
        background: #dce5ee !important;
    }

    /* Violations */
    .violation-card {
        background: #fff6f6 !important;
        border-color: #efb8bd !important;
    }

    .violation-title {
        color: #991b1b !important;
    }

    .violation-meta {
        color: #64748b !important;
    }

    .violation-meta strong {
        color: #334155 !important;
    }

    .safe-box {
        background: #f0faf3 !important;
        border-color: #acdcbf !important;
        color: #166534 !important;
    }

    .safe-box strong {
        color: #14532d !important;
    }

    /* Detection pills */
    .detection-pill {
        background: #ffffff !important;
        border-color: #cbd8e5 !important;
        color: #334155 !important;
        box-shadow: 0 2px 8px rgba(30, 55, 85, .04) !important;
    }

    .pill-count {
        color: #087aa9 !important;
    }

    /* Expander */
    [data-testid="stExpander"] {
        background: #ffffff !important;
        border-color: #cbd8e5 !important;
    }

    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p {
        color: #26364d !important;
        font-weight: 700 !important;
    }

    /* Details content */
    code {
        color: #075985 !important;
        background: #edf7fb !important;
    }

    /* Information box */
    .info-box {
        background: #ffffff !important;
        border-color: #ccd8e5 !important;
        color: #475569 !important;
    }

    .info-box strong {
        color: #1e293b !important;
    }

    /* Streamlit alerts */
    [data-testid="stAlert"] {
        color: #1e293b !important;
    }

    [data-testid="stAlert"] p {
        color: #334155 !important;
    }

    /* Footer */
    .footer {
        color: #64748b !important;
        border-top-color: #d8e1eb !important;
    }

    .footer strong {
        color: #334155 !important;
    }

    /* Sidebar — keep dark branding but increase contrast */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111a2b 0%, #0d1524 100%) !important;
    }

    section[data-testid="stSidebar"] .sidebar-brand-title {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] .sidebar-brand-sub {
        color: #9fb0c7 !important;
    }

    section[data-testid="stSidebar"] .sidebar-section-title {
        color: #dbe7f5 !important;
    }

    section[data-testid="stSidebar"] .class-row {
        color: #c4d0df !important;
    }

    section[data-testid="stSidebar"] .class-row:hover {
        background: #1b2940 !important;
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] .tech-chip {
        color: #c2cede !important;
        background: #17243a !important;
        border-color: #344760 !important;
    }

    section[data-testid="stSidebar"] .sidebar-footer {
        color: #8ea0b8 !important;
    }

    section[data-testid="stSidebar"] .sidebar-footer strong {
        color: #cbd8e8 !important;
    }

    /* Native Streamlit text in the main area */
    .main p,
    .main label,
    .main span {
        /* Intentionally not forcing every span: component-specific rules above win. */
    }

    /* Better readability on smaller screens */
    @media (max-width: 900px) {
        .hero-description,
        .hero-subtitle {
            color: #334155 !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# VALIDATE PROJECT
# ============================================================

try:
    validate_project_files()
except FileNotFoundError as error:
    st.error(str(error))
    st.stop()


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_detector():
    return SafeVisionDetector()


try:
    detector = load_detector()
except Exception as error:
    st.error(f"Failed to load SafeVision AI model: {error}")
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">🦺</div>
            <div>
                <div class="sidebar-brand-title">SafeVision AI</div>
                <div class="sidebar-brand-sub">COMPUTER VISION SAFETY</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="color:#7f8da3;font-size:.74rem;line-height:1.7;">
            Intelligent PPE detection and workplace safety analysis
            powered by deep learning.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">Detection Classes</div>',
                unsafe_allow_html=True)

    classes = [
        ("👤", "Person"),
        ("⛑️", "Helmet"),
        ("❌", "No Helmet"),
        ("🥽", "Goggles"),
        ("❌", "No Goggles"),
        ("🧤", "Gloves"),
        ("❌", "No Gloves"),
        ("🥾", "Boots"),
        ("🦺", "Vest"),
    ]

    for icon, name in classes:
        st.markdown(
            f"""
            <div class="class-row">
                <span class="class-icon">{icon}</span>
                <span>{name}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">Technology</div>',
                unsafe_allow_html=True)

    st.markdown(
        """
        <span class="tech-chip">YOLO11n</span>
        <span class="tech-chip">Ultralytics</span>
        <span class="tech-chip">PyTorch</span>
        <span class="tech-chip">OpenCV</span>
        <span class="tech-chip">Streamlit</span>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-footer">
            <strong>SafeVision AI</strong><br>
            End-to-end AI portfolio project<br>
            PPE Detection • Computer Vision • Safety Analytics
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-wrap">
        <div class="hero-eyebrow">● AI-POWERED WORKPLACE SAFETY</div>
        <h1 class="hero-title">SafeVision <span class="accent">AI</span></h1>
        <div class="hero-subtitle">
            Real-Time PPE &amp; Workplace Safety Detection
        </div>
        <div class="hero-description">
            An intelligent computer vision system that detects personal
            protective equipment and explicit workplace safety violations
            from workplace imagery using YOLO11n.
        </div>
        <div class="hero-tech">
            YOLO11n &nbsp;•&nbsp; Object Detection &nbsp;•&nbsp;
            PPE Compliance &nbsp;•&nbsp; Safety Analytics
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# UPLOAD
# ============================================================

st.markdown(
    """
    <div class="section-head">
        <div class="section-icon">📤</div>
        <div class="section-title">Analyze Workplace Image</div>
        <div class="section-caption">JPG • JPEG • PNG</div>
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Choose an image",
    type=SUPPORTED_IMAGE_TYPES,
    label_visibility="collapsed",
)

if uploaded_file is None:
    st.markdown(
        """
        <div class="info-box" style="margin-top:10px;">
            <strong>How SafeVision works</strong><br>
            Upload a workplace image and the AI pipeline will detect PPE,
            identify explicit violation classes, calculate measurable
            safety indicators, and generate an annotated result.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


# ============================================================
# LOAD IMAGE
# ============================================================

try:
    image = Image.open(uploaded_file).convert("RGB")
except Exception as error:
    st.error(f"Unable to read the uploaded image: {error}")
    st.stop()


# ============================================================
# INFERENCE
# ============================================================

with st.spinner("Running SafeVision AI inference..."):
    try:
        result = detector.predict(image)
    except Exception as error:
        st.error(f"Inference failed: {error}")
        st.stop()


# ============================================================
# RESULT DATA
# ============================================================

detections = result["detections"]
detection_count = result["detection_count"]
safety = result["safety"]
safety_score = safety["safety_score"]
score_status = safety["score_status"]
compliance = safety["compliance"]
violations = safety["violations"]
annotated_image = result["annotated_image"]


# ============================================================
# IMAGE COMPARISON
# ============================================================

st.markdown(
    """
    <div class="section-head">
        <div class="section-icon">🔍</div>
        <div class="section-title">Detection Results</div>
        <div class="section-caption">ORIGINAL VS AI ANNOTATED</div>
    </div>
    """,
    unsafe_allow_html=True,
)

image_col1, image_col2 = st.columns(2, gap="large")

with image_col1:
    st.markdown('<div class="image-card-title">Original Image</div>',
                unsafe_allow_html=True)
    st.image(image, use_container_width=True)

with image_col2:
    st.markdown('<div class="image-card-title">AI Annotated Image</div>',
                unsafe_allow_html=True)
    st.image(annotated_image, use_container_width=True)


# ============================================================
# SAFETY OVERVIEW
# ============================================================

st.markdown(
    """
    <div class="section-head">
        <div class="section-icon">🛡️</div>
        <div class="section-title">Safety Overview</div>
        <div class="section-caption">DETECTION-LEVEL ANALYTICS</div>
    </div>
    """,
    unsafe_allow_html=True,
)

score_display = "N/A" if safety_score is None else format_percentage(safety_score)

st.markdown(
    f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-label">SAFETY SCORE</div>
            <div class="metric-value">{score_display}</div>
            <div class="metric-hint">Overall measurable PPE compliance</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">TOTAL DETECTIONS</div>
            <div class="metric-value">{detection_count}</div>
            <div class="metric-hint">Objects detected by YOLO11n</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">CONFIRMED VIOLATIONS</div>
            <div class="metric-value">{len(violations)}</div>
            <div class="metric-hint">Explicit negative PPE classes</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SAFETY STATUS
# ============================================================

status = get_safety_status(safety_score, score_status)

if status == "Safe":
    status_class = ""
    status_icon = "🟢"
elif status == "Needs Attention":
    status_class = "status-attention"
    status_icon = "🟡"
elif status == "High Risk":
    status_class = "status-danger"
    status_icon = "🔴"
else:
    status_class = "status-attention"
    status_icon = "🔵"

st.markdown(
    f"""
    <div class="status-box {status_class}">
        <span class="status-dot"></span>
        <span>{status_icon} Safety Status: <strong>{status}</strong></span>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PPE COMPLIANCE
# ============================================================

st.markdown(
    """
    <div class="section-head">
        <div class="section-icon">🦺</div>
        <div class="section-title">PPE Compliance</div>
        <div class="section-caption">EQUIPMENT COVERAGE</div>
    </div>
    """,
    unsafe_allow_html=True,
)

compliance_columns = st.columns(5, gap="small")

for column, (requirement, value) in zip(
    compliance_columns,
    compliance.items(),
):
    with column:
        display_name = requirement.replace("_", " ").title()
        percentage = format_percentage(value)

        try:
            numeric_value = max(0.0, min(100.0, float(value)))
        except (TypeError, ValueError):
            numeric_value = 0.0

        st.markdown(
            f"""
            <div class="compliance-card">
                <div class="compliance-name">{display_name}</div>
                <div class="compliance-value">{percentage}</div>
                <div class="progress-track">
                    <div class="progress-fill" style="width:{numeric_value}%"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# VIOLATIONS
# ============================================================

st.markdown(
    """
    <div class="section-head">
        <div class="section-icon">🚨</div>
        <div class="section-title">Confirmed Safety Violations</div>
        <div class="section-caption">EXPLICIT NEGATIVE CLASSES</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if violations:
    for violation in violations:
        category = violation["category"]
        violation_class = violation["violation_class"]
        count = violation["count"]

        st.markdown(
            f"""
            <div class="violation-card">
                <div class="violation-title">
                    🚨 {category}
                </div>
                <div class="violation-meta">
                    Class <strong>{violation_class}</strong>
                    &nbsp;•&nbsp; {count} detection(s)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.markdown(
        """
        <div class="safe-box">
            🛡️ <strong>No explicit PPE violation classes were detected.</strong>
            The analyzed image contains no detected negative PPE class.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DETECTION SUMMARY
# ============================================================

st.markdown(
    """
    <div class="section-head">
        <div class="section-icon">📊</div>
        <div class="section-title">Detected Classes</div>
        <div class="section-caption">OBJECT SUMMARY</div>
    </div>
    """,
    unsafe_allow_html=True,
)

summary = get_detection_summary(detections)

if summary:
    pills = '<div class="pill-wrap">'
    for class_name, count in summary.items():
        pills += (
            f'<span class="detection-pill">'
            f'{class_name}'
            f'<span class="pill-count">{count}</span>'
            f'</span>'
        )
    pills += "</div>"
    st.markdown(pills, unsafe_allow_html=True)
else:
    st.info("No objects were detected.")


# ============================================================
# DETAILED DETECTIONS
# ============================================================

with st.expander("🔎  View Detailed Detections"):
    if detections:
        for index, detection in enumerate(detections, start=1):
            class_name = detection["class_name"]
            confidence = detection["confidence"]
            bbox = detection["bbox"]

            st.markdown(
                f"""
                <div style="
                    padding:9px 4px;
                    border-bottom:1px solid #e2e8f0;
                    color:#9aa8bc;
                    font-size:.75rem;">
                    <strong style="color:#dce4ef;">#{index} {class_name}</strong>
                    &nbsp;•&nbsp; Confidence:
                    <code>{confidence:.3f}</code>
                    &nbsp;•&nbsp; BBox:
                    <code>{bbox}</code>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.write("No detections available.")


# ============================================================
# INTERPRETATION NOTE
# ============================================================

st.markdown(
    """
    <div class="section-head">
        <div class="section-icon">ℹ️</div>
        <div class="section-title">Interpretation Note</div>
    </div>

    <div class="info-box">
        <strong>How to interpret the safety analytics</strong><br>
        Safety analytics are calculated at the detection level.
        Explicit negative PPE classes are treated as confirmed violations.
        Missing PPE detections are not automatically classified as violations
        when the dataset provides no explicit negative class.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <strong>SafeVision AI</strong>
        &nbsp;•&nbsp; YOLO11n
        &nbsp;•&nbsp; Computer Vision
        &nbsp;•&nbsp; PPE Detection
        &nbsp;•&nbsp; Safety Analytics
        <br>
        Built as an end-to-end AI portfolio project.
    </div>
    """,
    unsafe_allow_html=True,
)
