# ============================================================
# Main.py  —  Multi-Format AI Content Generator
# Pages: landing → signup/login → dashboard → generate → results
# ============================================================

import sys, os, json
from datetime import datetime
import streamlit as st

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from backend.image_generator import generate_cover_image
load_dotenv()

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Format AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Constants ────────────────────────────────────────────────
USERS_PATH = os.path.join(os.path.dirname(__file__), "..", "users.json")

AGENTS = [
    {"key": "blog",         "icon": "✍️",  "label": "BLOGGER",       "color": "#2563eb", "desc": "Writes a long-form blog article with structured headings."},
    {"key": "tweets",       "icon": "🐦",  "label": "TWEET CRAFTER", "color": "#0ea5e9", "desc": "Creates a viral tweet thread with hooks and CTAs."},
    {"key": "video_script", "icon": "🎥",  "label": "DIRECTOR",      "color": "#10b981", "desc": "Scripts a full video with stage directions."},
    {"key": "narration",    "icon": "🎙️", "label": "NARRATOR",      "color": "#f97316", "desc": "Crafts a 60-second short-form story narration."},
    {"key": "seo",          "icon": "🔍",  "label": "SEO ANALYST",   "color": "#ec4899", "desc": "Produces meta tags, keywords and SEO strategy."},
    {"key": "references",   "icon": "🔗",  "label": "RESEARCHER",    "color": "#8b5cf6", "desc": "Surfaces 6 high-quality credible references."},
]

# ── Full CSS Theme ───────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stSidebar"] { display: none; }

/* Page background */
.stApp { background: #07080f !important; color: #e2e8f0; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── NAV BAR ── */
.nav-bar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 16px 48px; border-bottom: 1px solid #1a1d35;
    background: rgba(7,8,15,0.95); position: sticky; top: 0; z-index: 999;
}
.nav-logo { display: flex; align-items: center; gap: 12px; }
.nav-logo-icon {
    width: 36px; height: 36px; border-radius: 8px;
    background: linear-gradient(135deg, #f97316, #ea580c);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; font-weight: 700;
}
.nav-logo-text { font-size: 15px; font-weight: 600; color: #fff; line-height: 1.2; }
.nav-logo-sub { font-size: 11px; color: #64748b; font-weight: 400; }
.nav-user-chip {
    background: #11131c; border: 1px solid #1e2235;
    border-radius: 100px; padding: 6px 16px;
    font-size: 13px; color: #94a3b8; display: flex; align-items: center; gap: 8px;
}
.nav-user-dot { width: 8px; height: 8px; border-radius: 50%; background: #22c55e; }

/* ── LANDING ── */
.hero-section {
    padding: 80px 48px 60px;
    display: flex; align-items: center; gap: 60px;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(249,115,22,0.1); border: 1px solid rgba(249,115,22,0.3);
    color: #f97316; padding: 6px 16px; border-radius: 100px;
    font-size: 12px; font-weight: 600; letter-spacing: 1px;
    margin-bottom: 24px;
}
.hero-title {
    font-size: 52px; font-weight: 800; line-height: 1.1;
    color: #ffffff; margin-bottom: 12px;
}
.hero-title .orange { color: #f97316; }
.hero-subtitle { font-size: 16px; color: #64748b; line-height: 1.7; margin-bottom: 36px; max-width: 520px; }
.hero-buttons { display: flex; gap: 12px; }
.btn-primary {
    background: linear-gradient(135deg, #f97316, #ea580c);
    color: #fff; padding: 14px 28px; border-radius: 8px;
    font-size: 15px; font-weight: 600; text-decoration: none;
    border: none; cursor: pointer; display: inline-flex; align-items: center; gap: 8px;
    transition: opacity 0.2s; white-space: nowrap;
}
.btn-secondary {
    background: transparent; color: #cbd5e1;
    padding: 14px 28px; border-radius: 8px; font-size: 15px; font-weight: 500;
    border: 1px solid #1e2235; cursor: pointer; white-space: nowrap;
}

/* Agent visual cards on hero right */
.agents-visual {
    display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
    min-width: 360px;
}
.agent-visual-card {
    background: #0f1020; border: 1px solid #1a1d35;
    border-radius: 12px; padding: 16px;
    border-left: 3px solid var(--agent-color);
}
.agent-visual-card .av-label {
    font-size: 10px; font-weight: 700; letter-spacing: 1px;
    color: var(--agent-color); margin-bottom: 4px;
}
.agent-visual-card .av-desc { font-size: 12px; color: #475569; }

/* Feature row */
.features-row {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 1px; background: #1a1d35;
    border-top: 1px solid #1a1d35; border-bottom: 1px solid #1a1d35;
}
.feature-item {
    background: #07080f; padding: 32px 40px;
    display: flex; flex-direction: column; gap: 8px;
}
.feature-item .fi-icon { font-size: 24px; }
.feature-item .fi-title { font-size: 15px; font-weight: 600; color: #e2e8f0; }
.feature-item .fi-desc { font-size: 13px; color: #475569; }

/* ── AUTH PAGES ── */
.auth-layout {
    display: grid; grid-template-columns: 1fr 1fr;
    min-height: calc(100vh - 65px);
}
.auth-left {
    background: #07080f; padding: 60px 64px;
    display: flex; flex-direction: column; justify-content: center;
}
.auth-left h1 { font-size: 36px; font-weight: 800; color: #fff; line-height: 1.2; margin-bottom: 16px; }
.auth-left p { font-size: 15px; color: #64748b; line-height: 1.7; margin-bottom: 40px; }
.auth-feature {
    background: #0f1020; border: 1px solid #1a1d35;
    border-radius: 10px; padding: 16px 20px; margin-bottom: 10px;
}
.auth-feature .af-title { font-size: 12px; font-weight: 700; letter-spacing: 1px; color: #f97316; margin-bottom: 4px; }
.auth-feature .af-desc { font-size: 13px; color: #64748b; }
.auth-right {
    background: #0a0b14; border-left: 1px solid #1a1d35;
    padding: 60px 64px; display: flex; flex-direction: column; justify-content: center;
}
.auth-form-label { font-size: 11px; font-weight: 700; color: #f97316; letter-spacing: 1px; margin-bottom: 24px; }
.auth-form-title { font-size: 28px; font-weight: 700; color: #fff; margin-bottom: 32px; }
.auth-form-footer { font-size: 13px; color: #64748b; text-align: center; margin-top: 16px; }

/* ── FORM INPUTS ── */
.stTextInput > div > div > input {
    background: #0f1020 !important; border: 1px solid #1e2235 !important;
    color: #e2e8f0 !important; border-radius: 8px !important;
    padding: 12px 16px !important; font-size: 14px !important;
    transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #f97316 !important; box-shadow: 0 0 0 2px rgba(249,115,22,0.15) !important;
}
.stTextInput label { color: #94a3b8 !important; font-size: 13px !important; font-weight: 500 !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #f97316, #ea580c) !important;
    color: #fff !important; border: none !important;
    border-radius: 8px !important; padding: 12px 24px !important;
    font-size: 15px !important; font-weight: 600 !important;
    width: 100% !important; transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stButton > button[kind="secondary"] {
    background: transparent !important; border: 1px solid #1e2235 !important;
    color: #94a3b8 !important;
}

/* ── DASHBOARD ── */
.dash-header {
    padding: 40px 48px 20px;
    border-bottom: 1px solid #1a1d35;
}
.dash-header .dh-badge {
    font-size: 11px; font-weight: 700; letter-spacing: 1px;
    color: #f97316; margin-bottom: 12px;
    display: flex; align-items: center; gap: 8px;
}
.dash-header h2 { font-size: 28px; font-weight: 700; color: #fff; margin-bottom: 8px; }
.dash-header p { font-size: 14px; color: #475569; }

/* Agent format cards */
.format-card {
    background: #0f1020; border: 1px solid #1a1d35;
    border-radius: 12px; padding: 20px;
    border-top: 3px solid var(--fc-color);
    height: 100%;
}
.format-card .fc-icon { font-size: 28px; margin-bottom: 10px; }
.format-card .fc-label {
    font-size: 11px; font-weight: 700; letter-spacing: 1px;
    color: var(--fc-color); margin-bottom: 6px;
}
.format-card .fc-desc { font-size: 12px; color: #475569; line-height: 1.5; }

/* Topic input area */
.topic-section {
    background: #0a0b14; border: 1px solid #1a1d35;
    border-radius: 12px; padding: 28px 32px; margin: 0 48px 32px;
}
.topic-section .ts-label {
    font-size: 11px; font-weight: 700; letter-spacing: 1px; color: #f97316; margin-bottom: 8px;
}
.topic-section .ts-title { font-size: 20px; font-weight: 700; color: #fff; margin-bottom: 8px; }
.topic-section .ts-desc { font-size: 13px; color: #64748b; margin-bottom: 20px; }
.stTextArea > div > div > textarea {
    background: #0f1020 !important; border: 1px solid #1e2235 !important;
    color: #e2e8f0 !important; border-radius: 8px !important;
    font-size: 14px !important; resize: none !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: #f97316 !important; box-shadow: 0 0 0 2px rgba(249,115,22,0.15) !important;
}
.stTextArea label { display: none !important; }

/* Topic chips */
.topic-chips { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px; }
.topic-chip {
    background: #11131c; border: 1px solid #1e2235;
    color: #64748b; padding: 6px 14px; border-radius: 100px;
    font-size: 12px; cursor: pointer;
}

/* ── GENERATION PAGE ── */
.gen-header {
    padding: 32px 48px 24px; border-bottom: 1px solid #1a1d35;
}
.gen-header h2 { font-size: 24px; font-weight: 700; color: #fff; }
.gen-header p { font-size: 14px; color: #475569; }

/* Pipeline card */
.pipeline-card {
    background: #0f1020; border: 1px solid #1a1d35;
    border-radius: 12px; padding: 18px 20px; margin-bottom: 10px;
    display: flex; align-items: center; gap: 14px;
}
.pipeline-card .pc-icon-wrap {
    width: 40px; height: 40px; border-radius: 10px;
    background: var(--pc-color-bg); border: 1px solid var(--pc-color);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
}
.pipeline-card .pc-info { flex: 1; }
.pipeline-card .pc-label {
    font-size: 11px; font-weight: 700; letter-spacing: 1px; color: var(--pc-color);
}
.pipeline-card .pc-status { font-size: 12px; color: #475569; margin-top: 2px; }
.pipeline-card .pc-badge {
    font-size: 11px; font-weight: 600; padding: 3px 10px;
    border-radius: 100px; white-space: nowrap;
}
.badge-queue { background: #1e2235; color: #475569; }
.badge-running { background: rgba(249,115,22,0.15); color: #f97316; }
.badge-done { background: rgba(34,197,94,0.15); color: #22c55e; }
.badge-skip { background: #1e2235; color: #334155; }

/* Live log */
.log-panel {
    background: #0a0b14; border: 1px solid #1a1d35;
    border-radius: 12px; padding: 16px;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px; line-height: 1.8; color: #475569;
    min-height: 200px; max-height: 400px; overflow-y: auto;
}

/* ── RESULTS PAGE ── */
.result-tab-content {
    background: #0f1020; border: 1px solid #1a1d35;
    border-radius: 12px; padding: 24px;
    white-space: pre-wrap; font-size: 14px; line-height: 1.8;
    color: #cbd5e1; max-height: 600px; overflow-y: auto;
    margin-top: 12px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1a1d35 !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #475569 !important; font-weight: 600 !important;
    font-size: 13px !important; border-radius: 6px 6px 0 0 !important;
    padding: 10px 18px !important;
}
.stTabs [aria-selected="true"] {
    color: #f97316 !important; border-bottom: 2px solid #f97316 !important;
    background: rgba(249,115,22,0.05) !important;
}

/* Toggle */
.stToggle label { color: #94a3b8 !important; font-size: 13px !important; }

/* Error / success */
.stAlert { border-radius: 8px !important; }

/* Divider */
hr { border-color: #1a1d35 !important; }

/* Download button */
.stDownloadButton > button {
    background: #11131c !important; color: #94a3b8 !important;
    border: 1px solid #1e2235 !important; font-size: 13px !important;
    padding: 8px 16px !important; width: auto !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════

def load_users():
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_user(name, email, password):
    users = load_users()
    users.append({"name": name, "email": email, "password": password})
    with open(USERS_PATH, "w") as f:
        json.dump(users, f, indent=4)

def authenticate(email, password):
    for u in load_users():
        if u["email"] == email and u["password"] == password:
            return u
    return None

def email_exists(email):
    return any(u["email"] == email for u in load_users())

def nav_bar(show_user=False):
    user_html = ""
    if show_user and st.session_state.get("user_name"):
        user_html = f'<div class="nav-user-chip"><div class="nav-user-dot"></div>{st.session_state.user_name}</div>'
    st.markdown(f"""
    <div class="nav-bar">
        <div class="nav-logo">
            <div class="nav-logo-icon">🤖</div>
            <div>
                <div class="nav-logo-text">Multi-Format AI</div>
                <div class="nav-logo-sub">Content Generation Platform</div>
            </div>
        </div>
        {user_html}
    </div>
    """, unsafe_allow_html=True)

def init_session():
    defaults = {
        "page": "landing",
        "logged_in": False,
        "user_name": "",
        "user_email": "",
        "topic": "",
        "selected_formats": {a["key"]: True for a in AGENTS},
        "results": {},
        "structure": {},
        "generation_logs": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def go(page):
    st.session_state.page = page
    st.rerun()


# ══════════════════════════════════════════════════════════════
# PAGE 1 — LANDING
# ══════════════════════════════════════════════════════════════

def landing_page():
    nav_bar()

    # Hero
    col_left, col_right = st.columns([1.1, 1], gap="large")
    with col_left:
        st.markdown("""
        <div style="padding: 60px 48px 40px;">
            <div class="hero-badge">⚡ AI CONTENT GENERATION PLATFORM</div>
            <div class="hero-title">
                Transform Any Idea Into<br>
                <span class="orange">6 Content Formats</span><br>
                Instantly.
            </div>
            <div class="hero-subtitle">
                Enter a single topic and watch AI simultaneously generate a blog article,
                tweet thread, video script, narration, SEO strategy, and references — 
                all in real-time with transparent prompt chaining.
            </div>
        </div>
        """, unsafe_allow_html=True)
        btn_col1, btn_col2, _ = st.columns([1, 1, 2])
        with btn_col1:
            if st.button("Create Account →"):
                go("signup")
        with btn_col2:
            if st.button("Sign In", type="secondary"):
                go("login")

    with col_right:
        st.markdown("""
        <div style="padding: 60px 48px 40px 24px;">
            <div class="agents-visual">
                <div class="agent-visual-card" style="--agent-color:#2563eb">
                    <div class="av-label">✍️ BLOGGER</div>
                    <div class="av-desc">Long-form article with structured headings</div>
                </div>
                <div class="agent-visual-card" style="--agent-color:#0ea5e9">
                    <div class="av-label">🐦 TWEET CRAFTER</div>
                    <div class="av-desc">Viral thread with hooks and CTAs</div>
                </div>
                <div class="agent-visual-card" style="--agent-color:#10b981">
                    <div class="av-label">🎥 DIRECTOR</div>
                    <div class="av-desc">Full video script with stage directions</div>
                </div>
                <div class="agent-visual-card" style="--agent-color:#f97316">
                    <div class="av-label">🎙️ NARRATOR</div>
                    <div class="av-desc">60-second short-form story</div>
                </div>
                <div class="agent-visual-card" style="--agent-color:#ec4899">
                    <div class="av-label">🔍 SEO ANALYST</div>
                    <div class="av-desc">Meta tags, keywords & strategy</div>
                </div>
                <div class="agent-visual-card" style="--agent-color:#8b5cf6">
                    <div class="av-label">🔗 RESEARCHER</div>
                    <div class="av-desc">6 credible, cited references</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Features row
    st.markdown("""
    <div class="features-row">
        <div class="feature-item">
            <div class="fi-icon">🔗</div>
            <div class="fi-title">Prompt Chaining</div>
            <div class="fi-desc">Sequential AI steps build context for each format</div>
        </div>
        <div class="feature-item">
            <div class="fi-icon">⚡</div>
            <div class="fi-title">Real-Time Streaming</div>
            <div class="fi-desc">Watch each format generate live with live logs</div>
        </div>
        <div class="feature-item">
            <div class="fi-icon">🎛️</div>
            <div class="fi-title">Selective Workflow</div>
            <div class="fi-desc">Toggle only the formats you need per run</div>
        </div>
        <div class="feature-item">
            <div class="fi-icon">⬇️</div>
            <div class="fi-title">Download All</div>
            <div class="fi-desc">Export every format as individual text files</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 2 — SIGN UP
# ══════════════════════════════════════════════════════════════

def signup_page():
    nav_bar()
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("""
        <div class="auth-left">
            <div style="margin-bottom:12px">
                <span style="font-size:11px;font-weight:700;letter-spacing:1px;color:#f97316">
                    🔐 CREATE YOUR ACCOUNT
                </span>
            </div>
            <h1>Build your content<br>generation workspace.</h1>
            <p>One account. Six AI-powered content formats.<br>Real-time generation with full transparency.</p>
            <div class="auth-feature">
                <div class="af-title">🔗 PROMPT CHAINING ENGINE</div>
                <div class="af-desc">Each format learns from the shared content structure</div>
            </div>
            <div class="auth-feature">
                <div class="af-title">⚡ LIVE STREAMING OUTPUT</div>
                <div class="af-desc">Watch generation happen word by word in real time</div>
            </div>
            <div class="auth-feature">
                <div class="af-title">🎛️ SELECTIVE WORKFLOWS</div>
                <div class="af-desc">Choose only the content formats you need per run</div>
            </div>
            <div class="auth-feature">
                <div class="af-title">⬇️ INSTANT DOWNLOADS</div>
                <div class="af-desc">Export each format as a clean text file</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div style="padding: 60px 64px;">
            <div class="auth-form-label">SIGN UP</div>
            <div class="auth-form-title">Create your account</div>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown('<div style="padding: 0 64px 60px;">', unsafe_allow_html=True)
            name = st.text_input("Full Name", placeholder="Sachin Chaudhary")
            email = st.text_input("Email", placeholder="name@example.com")
            password = st.text_input("Password", type="password", placeholder="Create a password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create Account →"):
                if not name or not email or not password:
                    st.error("Please fill in all fields.")
                elif email_exists(email):
                    st.error("An account with this email already exists.")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    save_user(name, email, password)
                    st.success("Account created! Redirecting to login...")
                    import time; time.sleep(1)
                    go("login")
            st.markdown('<div class="auth-form-footer">Already have an account? </div>', unsafe_allow_html=True)
            if st.button("Sign In instead", type="secondary"):
                go("login")
            if st.button("← Back to Home", type="secondary"):
                go("landing")
            st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 3 — LOGIN
# ══════════════════════════════════════════════════════════════

def login_page():
    nav_bar()
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("""
        <div class="auth-left">
            <div style="margin-bottom:12px">
                <span style="font-size:11px;font-weight:700;letter-spacing:1px;color:#f97316">
                    🔓 WELCOME BACK
                </span>
            </div>
            <h1>Sign in to continue<br>generating content.</h1>
            <p>Your topic becomes 6 platform-ready formats,<br>generated with transparent AI reasoning.</p>
            <div class="auth-feature">
                <div class="af-title">🔗 PROMPT CHAINING ENGINE</div>
                <div class="af-desc">Each format builds on a shared content plan</div>
            </div>
            <div class="auth-feature">
                <div class="af-title">⚡ LIVE STREAMING OUTPUT</div>
                <div class="af-desc">Watch generation happen in real time</div>
            </div>
            <div class="auth-feature">
                <div class="af-title">🎛️ SELECTIVE WORKFLOWS</div>
                <div class="af-desc">Toggle only the formats you need</div>
            </div>
            <div class="auth-feature">
                <div class="af-title">⬇️ INSTANT DOWNLOADS</div>
                <div class="af-desc">Export each format as a clean text file</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div style="padding: 60px 64px;">
            <div class="auth-form-label">LOGIN</div>
            <div class="auth-form-title">Access your workspace</div>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown('<div style="padding: 0 64px 60px;">', unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="name@example.com", key="login_email")
            password = st.text_input("Password", type="password", placeholder="Your password", key="login_pass")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In →"):
                if not email or not password:
                    st.error("Please enter your email and password.")
                else:
                    user = authenticate(email, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_name = user["name"]
                        st.session_state.user_email = user["email"]
                        go("dashboard")
                    else:
                        st.error("Incorrect email or password.")
            st.markdown('<div class="auth-form-footer">Need an account?</div>', unsafe_allow_html=True)
            if st.button("Create one →", type="secondary"):
                go("signup")
            if st.button("← Back to Home", type="secondary"):
                go("landing")
            st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 4 — DASHBOARD
# ══════════════════════════════════════════════════════════════

def dashboard_page():
    nav_bar(show_user=True)

    # Logout button
    _, logout_col = st.columns([8, 1])
    with logout_col:
        if st.button("Log Out"):
            st.session_state.logged_in = False
            go("landing")

    # Header
    st.markdown("""
    <div class="dash-header">
        <div class="dh-badge">🧠 CONTENT GENERATION ENGINE</div>
        <h2>Configure your content run</h2>
        <p>Select the formats you want, enter your topic, and launch your generation pipeline.<br>
        The AI will build a shared content plan first, then generate each format sequentially.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Format cards with toggles
    st.markdown('<div style="padding: 0 48px;">', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
        <div>
            <div style="font-size:11px;font-weight:700;letter-spacing:1px;color:#f97316;margin-bottom:4px">
                🎛️ SELECTIVE FORMAT EXECUTION
            </div>
            <div style="font-size:20px;font-weight:700;color:#fff;">Choose the formats you want to run</div>
            <div style="font-size:13px;color:#475569;margin-top:4px">
                Selected formats run in order. Toggled-off formats are skipped gracefully.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for i, agent in enumerate(AGENTS):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="format-card" style="--fc-color:{agent['color']}">
                <div class="fc-icon">{agent['icon']}</div>
                <div class="fc-label">{agent['label']}</div>
                <div class="fc-desc">{agent['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.selected_formats[agent["key"]] = st.toggle(
                "Include", value=st.session_state.selected_formats[agent["key"]],
                key=f"toggle_{agent['key']}"
            )

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Topic input section
    st.markdown("""
    <div class="topic-section">
        <div class="ts-label">📝 RESEARCH PROMPT</div>
        <div class="ts-title">Describe your content topic</div>
        <div class="ts-desc">
            Enter a topic, thesis, or idea. The more specific, the better the output quality.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div style="padding: 0 48px;">', unsafe_allow_html=True)
        topic = st.text_area(
            "topic_input",
            value=st.session_state.topic,
            placeholder="Example: How AI is transforming the FMCG supply chain in emerging markets...",
            height=100,
            key="topic_area"
        )

        # Example chips
        st.markdown("""
        <div class="topic-chips">
            <div class="topic-chip">AI in Healthcare</div>
            <div class="topic-chip">Rise of Electric Vehicles</div>
            <div class="topic-chip">Remote Work Future</div>
            <div class="topic-chip">Sustainable Fashion</div>
            <div class="topic-chip">Blockchain in Finance</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        selected_count = sum(st.session_state.selected_formats.values())
        col_info, col_btn = st.columns([3, 1])
        with col_info:
            st.markdown(f"""
            <div style="font-size:13px;color:#475569;padding-top:12px">
                ⚡ <strong style="color:#f97316">{selected_count} formats</strong> selected —
                pipeline will run sequentially with shared content plan
            </div>
            """, unsafe_allow_html=True)
        with col_btn:
            if st.button(f"🚀 Run Generation Pipeline"):
                if not topic.strip():
                    st.error("Please enter a topic first.")
                elif selected_count == 0:
                    st.error("Please select at least one format.")
                else:
                    st.session_state.topic = topic.strip()
                    st.session_state.results = {}
                    st.session_state.generation_logs = []
                    go("generate")

        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 5 — GENERATION (real-time streaming pipeline)
# ══════════════════════════════════════════════════════════════

def generate_page():
    from backend.generator import get_content_structure, stream_format, get_format_prompts

    nav_bar(show_user=True)

    st.markdown(f"""
    <div class="gen-header">
        <div style="font-size:11px;font-weight:700;letter-spacing:1px;color:#f97316;margin-bottom:8px">
            ⚡ AGENT WORKFLOW
        </div>
        <h2>Real-time pipeline running</h2>
        <p>Topic: <strong style="color:#e2e8f0">{st.session_state.topic}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_pipeline, col_output = st.columns([1, 1.6], gap="large")

    with col_pipeline:
        st.markdown('<div style="padding: 0 0 0 48px;">', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:11px;font-weight:700;letter-spacing:1px;color:#64748b;margin-bottom:12px">
            PIPELINE STATUS
        </div>
        """, unsafe_allow_html=True)

        # Planner card (always runs)
        planner_ph = st.empty()
        planner_ph.markdown("""
        <div class="pipeline-card" style="--pc-color:#f97316;--pc-color-bg:rgba(249,115,22,0.1)">
            <div class="pc-icon-wrap">📋</div>
            <div class="pc-info">
                <div class="pc-label">PLANNER</div>
                <div class="pc-status">Builds shared content structure</div>
            </div>
            <span class="pc-badge badge-queue">Queue</span>
        </div>
        """, unsafe_allow_html=True)

        agent_phs = {}
        for agent in AGENTS:
            agent_phs[agent["key"]] = st.empty()
            status = "Queue" if st.session_state.selected_formats.get(agent["key"]) else "Skip"
            badge_cls = "badge-queue" if status == "Queue" else "badge-skip"
            agent_phs[agent["key"]].markdown(f"""
            <div class="pipeline-card" style="--pc-color:{agent['color']};--pc-color-bg:{agent['color']}1a">
                <div class="pc-icon-wrap">{agent['icon']}</div>
                <div class="pc-info">
                    <div class="pc-label">{agent['label']}</div>
                    <div class="pc-status">{agent['desc'][:45]}...</div>
                </div>
                <span class="pc-badge {badge_cls}">{status}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:11px;font-weight:700;letter-spacing:1px;color:#64748b;margin-bottom:8px">LIVE AGENT LOGS</div>', unsafe_allow_html=True)
        log_ph = st.empty()
        log_ph.markdown('<div class="log-panel">Initializing pipeline...</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_output:
        st.markdown('<div style="padding-right: 48px;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:11px;font-weight:700;letter-spacing:1px;color:#64748b;margin-bottom:12px">LIVE OUTPUT</div>', unsafe_allow_html=True)
        output_label_ph = st.empty()
        output_ph = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── RUN THE PIPELINE ────────────────────────────────────
    logs = []
    results = {}

    def update_logs(msg):
        ts = datetime.now().strftime("%H:%M:%S")
        logs.append(f'<span style="color:#334155">{ts}</span> {msg}')
        log_ph.markdown(
            f'<div class="log-panel">' + "<br>".join(logs[-12:]) + '</div>',
            unsafe_allow_html=True
        )

    def set_card(ph, agent, status):
        badge_map = {
            "running": ("badge-running", "Running now."),
            "done":    ("badge-done",    "Completed ✓"),
            "skip":    ("badge-skip",    "Skipped"),
            "queue":   ("badge-queue",   "Queue"),
        }
        badge_cls, badge_txt = badge_map[status]
        ph.markdown(f"""
        <div class="pipeline-card" style="--pc-color:{agent['color']};--pc-color-bg:{agent['color']}1a">
            <div class="pc-icon-wrap">{agent['icon']}</div>
            <div class="pc-info">
                <div class="pc-label">{agent['label']}</div>
                <div class="pc-status">{agent['desc'][:45]}...</div>
            </div>
            <span class="pc-badge {badge_cls}">{badge_txt}</span>
        </div>
        """, unsafe_allow_html=True)

    # Step 1: Planner
    planner_ph.markdown("""
    <div class="pipeline-card" style="--pc-color:#f97316;--pc-color-bg:rgba(249,115,22,0.1)">
        <div class="pc-icon-wrap">📋</div>
        <div class="pc-info">
            <div class="pc-label">PLANNER</div>
            <div class="pc-status">Builds shared content structure</div>
        </div>
        <span class="pc-badge badge-running">Running now.</span>
    </div>
    """, unsafe_allow_html=True)

    update_logs('<span style="color:#f97316;font-weight:600">PLANNER</span> → Analyzing topic and building content structure...')
    output_label_ph.markdown('<div style="font-size:13px;font-weight:600;color:#f97316;margin-bottom:8px">📋 PLANNER — Building content structure...</div>', unsafe_allow_html=True)

    try:
        structure = get_content_structure(st.session_state.topic)
        st.session_state.structure = structure
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        st.info("👆 Check your .env file — make sure OPENAI_API_KEY has your valid API key.")
        if st.button("← Back to Dashboard"):
            go("dashboard")
        return

    planner_ph.markdown("""
    <div class="pipeline-card" style="--pc-color:#f97316;--pc-color-bg:rgba(249,115,22,0.1)">
        <div class="pc-icon-wrap">📋</div>
        <div class="pc-info">
            <div class="pc-label">PLANNER</div>
            <div class="pc-status">Builds shared content structure</div>
        </div>
        <span class="pc-badge badge-done">Completed ✓</span>
    </div>
    """, unsafe_allow_html=True)

    kp = structure.get("key_points", [])
    update_logs(f'<span style="color:#22c55e;font-weight:600">PLANNER ✓</span> → Structured {len(kp)} key points | Tone: {structure.get("tone","—")}')

    # Step 2: Run each format
    format_prompts = get_format_prompts(st.session_state.topic, structure)

    for agent in AGENTS:
        key = agent["key"]
        if not st.session_state.selected_formats.get(key):
            set_card(agent_phs[key], agent, "skip")
            update_logs(f'<span style="color:#334155">{agent["label"]}</span> → Skipped')
            continue

        set_card(agent_phs[key], agent, "running")
        update_logs(f'<span style="color:{agent["color"]};font-weight:600">{agent["label"]}</span> → Generating...')
        output_label_ph.markdown(f'<div style="font-size:13px;font-weight:600;color:{agent["color"]};margin-bottom:8px">{agent["icon"]} {agent["label"]} — Streaming output...</div>', unsafe_allow_html=True)

        prompt, max_tok = format_prompts[key]

        # Stream into the output panel
        full_text = output_ph.write_stream(stream_format(prompt, max_tok))
        results[key] = full_text

        set_card(agent_phs[key], agent, "done")
        word_count = len(full_text.split())
        update_logs(f'<span style="color:#22c55e;font-weight:600">{agent["label"]} ✓</span> → {word_count} words generated')

    # Done
    st.session_state.results = results
    update_logs('<span style="color:#22c55e;font-weight:700">✅ ALL FORMATS COMPLETE</span> — Pipeline finished successfully')
    output_label_ph.markdown('<div style="font-size:13px;font-weight:600;color:#22c55e;margin-bottom:8px">✅ Generation Complete!</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, center, _ = st.columns([2, 2, 2])
    with center:
        if st.button("📄 View All Results →"):
            go("results")


# ══════════════════════════════════════════════════════════════
# PAGE 6 — RESULTS
# ══════════════════════════════════════════════════════════════

def results_page():
    nav_bar(show_user=True)

    structure = st.session_state.get("structure", {})
    results = st.session_state.get("results", {})

    st.markdown(f"""
    <div style="padding: 32px 48px 0;">
        <div style="font-size:11px;font-weight:700;letter-spacing:1px;color:#f97316;margin-bottom:8px">
            📄 GENERATED CONTENT
        </div>
        <div style="font-size:26px;font-weight:700;color:#fff;margin-bottom:4px">
            {structure.get('title', st.session_state.topic)}
        </div>
        <div style="font-size:13px;color:#475569">
            Audience: {structure.get('target_audience','—')} &nbsp;·&nbsp;
            Tone: {structure.get('tone','—')} &nbsp;·&nbsp;
            {len(results)} formats generated
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Key points as chips
    if structure.get("key_points"):
        chips = " ".join([
            f'<span style="background:#11131c;border:1px solid #1e2235;color:#64748b;padding:4px 12px;border-radius:100px;font-size:11px;margin-right:6px">{p}</span>'
            for p in structure["key_points"]
        ])
        st.markdown(f'<div style="padding:0 48px 24px">{chips}</div>', unsafe_allow_html=True)

    tab_icons = {"blog":"✍️","tweets":"🐦","video_script":"🎥","narration":"🎙️","seo":"🔍","references":"🔗"}
    tab_labels = {"blog":"Blog Article","tweets":"Tweet Thread","video_script":"Video Script",
                  "narration":"Narration","seo":"SEO","references":"References"}

    active_results = {k: v for k, v in results.items() if v}

    # AI Cover Image

    topic = st.session_state.get("topic", "")

    if topic:

        with st.spinner("🎨 Generating AI cover image..."):

            image_bytes = generate_cover_image(topic)

        st.image(
        image_bytes,
        caption="AI Generated Cover Image",
        use_container_width=True
        )

    if not active_results:
        st.warning("No results found. Please run generation again.")
    else:
        tabs = st.tabs([f"{tab_icons.get(k,'📄')} {tab_labels.get(k,k.title())}" for k in active_results])
        for tab, (key, content) in zip(tabs, active_results.items()):
            with tab:
                agent = next((a for a in AGENTS if a["key"] == key), None)
                color = agent["color"] if agent else "#f97316"
                label = agent["label"] if agent else key.upper()
                st.markdown(f"""
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
                    <div>
                        <span style="font-size:11px;font-weight:700;letter-spacing:1px;color:{color}">{label}</span>
                        <div style="font-size:13px;color:#475569;margin-top:2px">{len(content.split())} words generated</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f'<div class="result-tab-content">{content}</div>', unsafe_allow_html=True)
                st.download_button(
                    f"⬇️ Download {tab_labels.get(key, key)}",
                    content,
                    file_name=f"{key}_{st.session_state.topic[:20].replace(' ','_')}.txt",
                    mime="text/plain",
                    key=f"dl_{key}"
                )

    st.markdown("<br><hr>", unsafe_allow_html=True)
    col1, col2, _ = st.columns([1.5, 1.5, 4])
    with col1:
        if st.button("🔄 Generate New Topic"):
            st.session_state.results = {}
            st.session_state.topic = ""
            go("dashboard")
    with col2:
        if st.button("← Back to Dashboard"):
            go("dashboard")


# ══════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════

def main():
    init_session()

    # Guard: redirect to login if trying to access protected pages
    protected = {"dashboard", "generate", "results"}
    if st.session_state.page in protected and not st.session_state.logged_in:
        st.session_state.page = "login"

    page = st.session_state.page
    if page == "landing":   landing_page()
    elif page == "signup":  signup_page()
    elif page == "login":   login_page()
    elif page == "dashboard": dashboard_page()
    elif page == "generate":  generate_page()
    elif page == "results":   results_page()

if __name__ == "__main__":
    main()
