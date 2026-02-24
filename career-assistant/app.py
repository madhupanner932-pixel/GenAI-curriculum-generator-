"""
app.py — Career Assistant Platform
Main Streamlit entry point.

Run with: streamlit run app.py
"""

import streamlit as st

# ── Page config (MUST be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Career Assistant — AI-Powered Career Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Module imports ─────────────────────────────────────────────────────────────
from modules.roadmap    import render_roadmap
from modules.chat       import render_chat
from modules.projects   import render_projects
from modules.resume     import render_resume
from modules.interview  import render_interview
from modules.skills     import render_skills
from modules.progress   import render_progress
from modules.gap_analysis import render_gap_analysis
from modules.achievements import render_achievements_page
from modules.resume_gap_analyzer import render_resume_gap_analyzer
from modules.market_trends import render_market_trends
from modules.adaptive_planner import render_adaptive_planner
from modules.user_history import render_user_history
from utils.profile_manager import ProfileManager
from utils.translations import get_text, get_all_translations

# ── Initialize session state ──────────────────────────────────────────────────
if "current_profile" not in st.session_state:
    st.session_state.current_profile = None
if "profile_manager" not in st.session_state:
    st.session_state.profile_manager = ProfileManager()
if "language" not in st.session_state:
    st.session_state.language = "en"

# ── Global Custom CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ─────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Root / Theme ─────────────────────────────────── */
:root {
    --primary:       #6C63FF;
    --primary-light: #8B85FF;
    --secondary:     #FF6584;
    --accent:        #43E97B;
    --bg-dark:       #0D0E1A;
    --bg-card:       #141528;
    --bg-glass:      rgba(20, 21, 40, 0.85);
    --border:        rgba(108, 99, 255, 0.25);
    --text-primary:  #F0F0FF;
    --text-muted:    #8888AA;
    --gradient-1:    linear-gradient(135deg, #6C63FF 0%, #FF6584 100%);
    --gradient-2:    linear-gradient(135deg, #43E97B 0%, #38F9D7 100%);
    --gradient-3:    linear-gradient(135deg, #FA8231 0%, #F7B731 100%);
    --shadow-glow:   0 0 30px rgba(108, 99, 255, 0.3);
}

/* ── Global Overrides ─────────────────────────────── */
html, body, .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg-dark) !important;
    color: var(--text-primary) !important;
}
.main .block-container {
    padding: 1.5rem 2.5rem !important;
    max-width: 1200px;
}

/* ── Sidebar ──────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f102a 0%, #161730 100%) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text-primary) !important;
}
.sidebar-logo {
    text-align: center;
    padding: 1.2rem 0.5rem 0.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}
.sidebar-logo .logo-icon {
    font-size: 2.8rem;
    line-height: 1;
}
.sidebar-logo h2 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.3rem 0 0.1rem;
}
.sidebar-logo p {
    font-size: 0.72rem;
    color: var(--text-muted) !important;
    margin: 0;
}

/* ── Nav Buttons ──────────────────────────────────── */
.nav-button {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    width: 100%;
    padding: 0.7rem 1rem;
    margin-bottom: 0.35rem;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s ease;
    color: var(--text-muted);
    font-size: 0.9rem;
    font-weight: 500;
    border: 1px solid transparent;
    text-decoration: none;
}
.nav-button:hover,
.nav-button.active {
    background: rgba(108, 99, 255, 0.15);
    border-color: var(--border);
    color: var(--text-primary);
}
.nav-button.active {
    background: rgba(108, 99, 255, 0.25);
    border-color: var(--primary);
    box-shadow: 0 0 0 1px rgba(108, 99, 255, 0.2);
}

/* ── Streamlit Radio (used as nav) ────────────────── */
div[data-testid="stRadio"] > label {
    display: none;
}
div[data-testid="stRadio"] > div {
    flex-direction: column !important;
    gap: 0.3rem !important;
}
div[data-testid="stRadio"] > div > label {
    display: flex !important;
    align-items: center !important;
    padding: 0.65rem 1rem !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    border: 1px solid transparent !important;
    transition: all 0.2s ease !important;
    margin: 0 !important;
}
div[data-testid="stRadio"] > div > label:hover {
    background: rgba(108, 99, 255, 0.15) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
}
div[data-testid="stRadio"] > div > label[data-baseweb="radio"] input:checked + div,
div[data-testid="stRadio"] > div > label[aria-checked="true"] {
    background: rgba(108, 99, 255, 0.25) !important;
    border-color: var(--primary) !important;
    color: var(--text-primary) !important;
}

/* ── Module Header ────────────────────────────────── */
.module-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: linear-gradient(135deg, rgba(108,99,255,0.15), rgba(255,101,132,0.08));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
}
.module-header .module-icon {
    font-size: 2.5rem;
    line-height: 1;
}
.module-header h2 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary) !important;
    margin: 0 0 0.2rem;
}
.module-header p {
    color: var(--text-muted) !important;
    margin: 0;
    font-size: 0.9rem;
}

/* ── Form Elements ────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background-color: rgba(20, 21, 40, 0.9) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.2) !important;
}

/* ── Buttons ──────────────────────────────────────── */
.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: var(--gradient-1) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.5rem !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3) !important;
}
.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(108, 99, 255, 0.5) !important;
}
.stButton > button[kind="secondary"],
.stFormSubmitButton > button[kind="secondary"],
.stButton > button:not([kind="primary"]) {
    background: rgba(108, 99, 255, 0.12) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: rgba(108, 99, 255, 0.22) !important;
    border-color: var(--primary) !important;
}
.stDownloadButton > button {
    background: rgba(67, 233, 123, 0.12) !important;
    border: 1px solid rgba(67, 233, 123, 0.3) !important;
    color: var(--accent) !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
}

/* ── Labels & Text ────────────────────────────────── */
.stSelectbox label, .stTextInput label, .stTextArea label,
.stMultiSelect label, .stSlider label {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
}
p, .stMarkdown p { color: var(--text-primary) !important; }
.stCaption { color: var(--text-muted) !important; }

/* ── Alerts ───────────────────────────────────────── */
.stSuccess > div {
    background: rgba(67, 233, 123, 0.12) !important;
    border: 1px solid rgba(67, 233, 123, 0.3) !important;
    border-radius: 10px !important;
    color: #43E97B !important;
}
.stError > div {
    background: rgba(255, 101, 132, 0.12) !important;
    border: 1px solid rgba(255, 101, 132, 0.3) !important;
    border-radius: 10px !important;
}
.stWarning > div {
    background: rgba(255, 177, 66, 0.12) !important;
    border: 1px solid rgba(255, 177, 66, 0.3) !important;
    border-radius: 10px !important;
}

/* ── Spinner ──────────────────────────────────────── */
.stSpinner > div {
    border-top-color: var(--primary) !important;
}

/* ── Custom Cards & Boxes ─────────────────────────── */
.tips-box {
    background: rgba(108, 99, 255, 0.08);
    border: 1px solid var(--border);
    border-left: 4px solid var(--primary);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
}
.tips-box h4 {
    color: var(--primary-light) !important;
    margin: 0 0 0.8rem;
    font-family: 'Space Grotesk', sans-serif;
}
.tips-box ul { margin: 0; padding-left: 1.2rem; }
.tips-box li { color: var(--text-primary) !important; margin-bottom: 0.4rem; }

/* ── Info Cards (3-column) ────────────────────────── */
.info-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    height: 100%;
}
.info-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-glow);
}
.info-card-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.info-card h4 {
    color: var(--text-primary) !important;
    font-size: 0.95rem;
    font-weight: 600;
    margin: 0 0 0.4rem;
}
.info-card p {
    color: var(--text-muted) !important;
    font-size: 0.82rem;
    margin: 0;
    line-height: 1.5;
}

/* ── Chat Empty State ─────────────────────────────── */
.chat-empty-state {
    text-align: center;
    padding: 3rem 2rem;
    color: var(--text-muted);
}
.chat-empty-state h4 { color: var(--text-primary) !important; font-size: 1.2rem; }
.chat-empty-state p  { margin: 0.5rem 0 1.5rem; }
.suggested-questions {
    text-align: left;
    max-width: 450px;
    margin: 0 auto;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.5rem;
}
.suggested-questions strong { color: var(--primary-light) !important; }
.suggested-questions ul { margin: 0.5rem 0 0; padding-left: 1.2rem; }
.suggested-questions li { color: var(--text-primary) !important; margin-bottom: 0.35rem; font-size: 0.875rem; }

/* ── Chat Messages ────────────────────────────────── */
[data-testid="stChatMessage"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    margin-bottom: 0.75rem !important;
    padding: 0.75rem 1rem !important;
}

/* ── Interview Question Card ──────────────────────── */
.question-card {
    background: linear-gradient(135deg, rgba(108,99,255,0.12), rgba(255,101,132,0.06));
    border: 1px solid var(--border);
    border-left: 4px solid var(--primary);
    border-radius: 14px;
    padding: 1.5rem;
    margin: 1rem 0 1.5rem;
}
.q-type-badge {
    display: inline-block;
    background: rgba(108, 99, 255, 0.2);
    color: var(--primary-light);
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    border: 1px solid rgba(108, 99, 255, 0.3);
    margin-bottom: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.question-card h3 {
    color: var(--text-muted) !important;
    font-size: 0.8rem;
    font-weight: 500;
    margin: 0 0 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.question-text {
    color: var(--text-primary) !important;
    font-size: 1.05rem !important;
    font-weight: 500 !important;
    line-height: 1.6 !important;
    margin: 0 !important;
}

/* ── Metrics ──────────────────────────────────────── */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
[data-testid="metric-container"] label { color: var(--text-muted) !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
}

/* ── Progress Bar ─────────────────────────────────── */
.stProgress > div > div > div {
    background: var(--gradient-1) !important;
    border-radius: 4px !important;
}

/* ── Expander ─────────────────────────────────────── */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

/* ── Divider ──────────────────────────────────────── */
hr { border-color: var(--border) !important; }

/* ── Slider ───────────────────────────────────────── */
.stSlider > div > div > div > div { background: var(--primary) !important; }

/* ── Scrollbar ────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-dark); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary); }

/* ── Config Banner ────────────────────────────────── */
.config-banner {
    background: rgba(255, 177, 66, 0.1);
    border: 1px solid rgba(255, 177, 66, 0.3);
    border-radius: 10px;
    padding: 0.8rem 1.2rem;
    margin-bottom: 1rem;
    font-size: 0.85rem;
    color: #FFB142 !important;
}
.config-banner a { color: #F7B731 !important; }

/* ── Tabs Styling ─────────────────────────────────── */
[data-testid="stTabs"] {
    background: transparent !important;
}
[data-testid="stTabs"] > div > div {
    border-bottom: 1px solid var(--border) !important;
}
[data-testid="stTabs"] button {
    color: var(--text-muted) !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
[data-testid="stTabs"] button:hover {
    color: var(--text-primary) !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--primary) !important;
    border-bottom-color: var(--primary) !important;
}

/* ── Data Frame Styling ───────────────────────────── */
[data-testid="stDataFrame"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
[data-testid="stDataFrame"] > div > div > table {
    font-size: 0.875rem !important;
}

/* ── Columns Enhancement ──────────────────────────── */
.stColumn {
    padding: 0.5rem !important;
}

/* ── Card Container ───────────────────────────────── */
.card-container {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.5rem;
    margin: 1rem 0;
    transition: all 0.3s ease;
}
.card-container:hover {
    border-color: var(--primary);
    box-shadow: 0 0 20px rgba(108, 99, 255, 0.15);
}

/* ── Achievement Badge ────────────────────────────── */
.achievement-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(67,233,123,0.2), rgba(56,249,215,0.1));
    border: 1px solid rgba(67,233,123,.3);
    border-radius: 20px;
    padding: 0.4rem 1rem;
    font-size: 0.8rem;
    font-weight: 600;
    color: #43E97B;
    margin: 0.2rem;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Responsive adjustments ───────────────────────── */
@media (max-width: 768px) {
    .main .block-container { padding: 1rem 1rem !important; }
    .module-header { flex-direction: column; text-align: center; }
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-icon">🚀</div>
        <h2>Career Assistant</h2>
        <p>AI-Powered Career Guidance Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ── Language Selection ─────────────────────────────────────────────────────
    st.markdown("### 🌐 Language / மொழி")
    
    lang_col1, lang_col2 = st.columns(2)
    with lang_col1:
        if st.button("🇬🇧 English", use_container_width=True, key="lang_en"):
            st.session_state.language = "en"
            st.rerun()
    with lang_col2:
        if st.button("🇮🇳 தமிழ்", use_container_width=True, key="lang_ta"):
            st.session_state.language = "ta"
            st.rerun()
    
    current_lang = "தமிழ் (Tamil)" if st.session_state.language == "ta" else "English"
    st.caption(f"Current: {current_lang}")
    
    st.markdown("---")

    # ── Profile Management ─────────────────────────────────────────────────────
    st.markdown(f"### {get_text('profile_management', st.session_state.language)}")
    
    pm = st.session_state.profile_manager
    profiles = pm.list_profiles()
    profile_names = [p["name"] for p in profiles]
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if profile_names:
            selected_profile = st.selectbox(
                get_text("select_profile", st.session_state.language),
                options=profile_names,
                label_visibility="collapsed"
            )
            if selected_profile:
                st.session_state.current_profile = pm.load_profile(selected_profile)
                st.success(f"✅ {get_text('profile_loaded', st.session_state.language)} {selected_profile}")
        else:
            st.info(get_text("no_profiles", st.session_state.language))
    
    with col2:
        if st.button("🗑️", help=get_text("delete_profile", st.session_state.language)):
            if st.session_state.current_profile:
                if pm.delete_profile(st.session_state.current_profile["name"]):
                    st.session_state.current_profile = None
                    st.rerun()
    
    # ── Create New Profile ────────────────────────────────────────────────────
    with st.expander(get_text("create_new_profile", st.session_state.language), expanded=not profile_names):
        with st.form("new_profile_form"):
            profile_name = st.text_input(
                get_text("profile_name", st.session_state.language),
                placeholder="e.g., John Doe" if st.session_state.language == "en" else "உதா: ஜான் டோ",
                help="Unique identifier for your career profile" if st.session_state.language == "en" else "உங்கள் தொழில் சுயவிவரத்திற்கான தனிப்பட்ட அடையாளம்"
            )
            career_field = st.selectbox(
                get_text("career_field", st.session_state.language),
                [
                    "Software Engineering",
                    "Data Science",
                    "Product Management",
                    "UX/UI Design",
                    "DevOps",
                    "Cloud Architecture",
                    "Machine Learning",
                    "Full Stack Web Dev",
                    "Mobile Development",
                    "Other"
                ]
            )
            experience_level = st.select_slider(
                get_text("experience_level", st.session_state.language),
                options=["Beginner", "Intermediate", "Advanced", "Expert"],
                value="Intermediate"
            )
            goals = st.text_area(
                get_text("career_goals", st.session_state.language),
                placeholder="What do you want to achieve?" if st.session_state.language == "en" else "நீங்கள் என்ன சாதிக்க விரும்புகிறீர்கள்?",
                help="Describe your short-term and long-term goals" if st.session_state.language == "en" else "உங்கள் குறுகிய மற்றும் நீண்ட கால லক்ষ்யங்களை விவரிக்கவும்"
            )
            
            if st.form_submit_button(get_text("create_profile", st.session_state.language)):
                if profile_name:
                    new_profile = pm.create_profile(
                        profile_name,
                        {
                            "career_field": career_field,
                            "experience_level": experience_level,
                            "goals": goals,
                            "skill_assessment": {},
                            "progress_data": [],
                        }
                    )
                    st.session_state.current_profile = new_profile
                    st.success(get_text("profile_created_success", st.session_state.language))
                    st.rerun()
                else:
                    st.error("Please enter a profile name" if st.session_state.language == "en" else "சுயவிவர பெயரை உள்ளிடவும்")
    
    # ── Current Profile Status ────────────────────────────────────────────────
    if st.session_state.current_profile:
        st.markdown("---")
        st.markdown(f"### {get_text('current_profile', st.session_state.language)}")
        profile = st.session_state.current_profile
        
        name_label = get_text("profile_name_label", st.session_state.language)
        field_label = get_text("profile_field_label", st.session_state.language)
        level_label = get_text("profile_level_label", st.session_state.language)
        
        st.markdown(f"""
        **{name_label}** {profile.get('name', 'N/A')}  
        **{field_label}** {profile.get('career_field', 'N/A')}  
        **{level_label}** {profile.get('experience_level', 'N/A')}  
        """)

    page = st.radio(
        "Navigation",
        options=[
            "🗺️  Career Roadmap",
            "💬  Smart Chat",
            "💡  Project Ideas",
            "📄  Resume Analyzer",
            "🎤  Mock Interview",
            "🎯  Skill Assessment",
            "📊  Progress & Analytics",
            "⚙️  Gap Analysis",
            "🏆  Achievements",
            "📋  Resume Gap Analyzer",
            "📈  Market Trends",
            "📅  Adaptive Planner",
            "📊  Activity History",
        ],
        label_visibility="collapsed"
    )

    # ── API Status indicator ──────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(f"### {get_text('configuration', st.session_state.language)}")

    from config import LLM_PROVIDER, GROQ_API_KEY, OPENAI_API_KEY, HF_API_KEY
    provider_labels = {
        "groq": ("🟢 Groq", GROQ_API_KEY),
        "openai": ("🔵 OpenAI", OPENAI_API_KEY),
        "huggingface": ("🟡 HuggingFace", HF_API_KEY),
    }
    label, key = provider_labels.get(LLM_PROVIDER.lower(), ("❓ Unknown", ""))
    key_ok = bool(key and key != "")

    st.markdown(f"**Provider:** {label}")
    if key_ok:
        st.success("✅ API key configured" if st.session_state.language == "en" else "✅ API விசை உள்ளமைக்கப்பட்டுள்ளது")
    else:
        st.warning("⚠️ API key missing" if st.session_state.language == "en" else "⚠️ API விசை விடுபட்டுள்ளது")
        st.caption("Add your key to `.env` file." if st.session_state.language == "en" else "உங்கள் விசையை `.env` கோப்பில் சேர்க்கவும்.")

    # ── Quick Setup Guide ─────────────────────────────────────────────────────
    with st.expander("📖 Quick Setup Guide" if st.session_state.language == "en" else "📖 விரைவு அமைப்பு வழிகாட்டி"):
        setup_text = """
        1. Create a `.env` file in the project folder
        2. Add your API key:
        ```
        # For Groq (free, recommended):
        LLM_PROVIDER=groq
        GROQ_API_KEY=your_key_here

        # For OpenAI:
        LLM_PROVIDER=openai
        OPENAI_API_KEY=your_key_here
        ```
        3. Get a free Groq key at [console.groq.com](https://console.groq.com)
        4. Restart the app
        """ if st.session_state.language == "en" else """
        1. திட்ட கோப்புறையில் `.env` கோப்பை உருவாக்கவும்
        2. உங்கள் API விசையைச் சேர்க்கவும்:
        ```
        # Groq க்கு (இலவசம், பரிந்துரைக்கப்பட்ட):
        LLM_PROVIDER=groq
        GROQ_API_KEY=your_key_here

        # OpenAI க்கு:
        LLM_PROVIDER=openai
        OPENAI_API_KEY=your_key_here
        ```
        3. [console.groq.com](https://console.groq.com) இல் இலவச Groq விசை பெறவும்
        4. பயன்பாட்டை மீண்டும் தொடங்கவும்
        """
        st.markdown(setup_text)

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.75rem; padding: 0.5rem 0;">
        Career Assistant v2.0<br>
        Built with Streamlit + AI
    </div>
    """, unsafe_allow_html=True)


# ── Main Content Router ───────────────────────────────────────────────────────
page_key = page.split("  ")[1].strip() if "  " in page else page.strip()

if page_key == "Career Roadmap":
    render_roadmap()
elif page_key == "Smart Chat":
    render_chat()
elif page_key == "Project Ideas":
    render_projects()
elif page_key == "Resume Analyzer":
    render_resume()
elif page_key == "Mock Interview":
    render_interview()
elif page_key == "Skill Assessment":
    render_skills()
elif page_key == "Progress & Analytics":
    render_progress()
elif page_key == "Gap Analysis":
    render_gap_analysis()
elif page_key == "Achievements":
    render_achievements_page()
elif page_key == "Resume Gap Analyzer":
    render_resume_gap_analyzer()
elif page_key == "Market Trends":
    render_market_trends()
elif page_key == "Adaptive Planner":
    render_adaptive_planner()
elif page_key == "Activity History":
    render_user_history()