import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from utils.llm import query_model
from utils.prompts import (
    get_roadmap_prompt, get_chat_prompt, get_projects_prompt,
    get_resume_prompt, get_interview_prompt, get_followup_prompt
)
from utils.storage import (
    save_profile, load_profile, get_all_profiles, delete_profile,
    save_roadmap, save_resume_analysis, save_interview_session,
    get_profile_stats, export_profile_as_text
)
from utils.assessment import get_assessment, calculate_score, get_skill_level, get_available_topics
from utils.visualizations import (
    format_stats_for_display, calculate_engagement_score,
    get_next_recommended_action, generate_progress_summary
)
from utils.reports import (
    generate_text_report, generate_csv_export, generate_json_export,
    generate_summary_stats, get_engagement_level
)

# Page configuration
st.set_page_config(
    page_title="Career Assistant Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    :root {
        --primary-color: #00D9FF;
        --background-color: #0a0e27;
        --secondary-color: #1f2937;
    }
    
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        color: #f0f4f8;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1f2937;
        border-radius: 4px 4px 0px 0px;
        color: #f0f4f8;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #00D9FF;
        color: #0a0e27;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #00D9FF;
        color: #f0f4f8;
    }
    
    h1, h2, h3 {
        color: #00D9FF;
    }
    
    .stButton > button {
        background-color: #00D9FF;
        color: #0a0e27;
        font-weight: 600;
        border: none;
        border-radius: 4px;
        padding: 10px 24px;
    }
    
    .stButton > button:hover {
        background-color: #00b8d4;
    }
    
    .success-box {
        background-color: #1a3a2a;
        padding: 15px;
        border-radius: 4px;
        border-left: 4px solid #10b981;
        color: #d1fae5;
    }
    
    .info-box {
        background-color: #1e3a5f;
        padding: 15px;
        border-radius: 4px;
        border-left: 4px solid #3b82f6;
        color: #dbeafe;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "current_profile" not in st.session_state:
    st.session_state.current_profile = None
if "profiles" not in st.session_state:
    st.session_state.profiles = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "roadmap_data" not in st.session_state:
    st.session_state.roadmap_data = None
if "profile_config" not in st.session_state:
    st.session_state.profile_config = {}
if "projects_data" not in st.session_state:
    st.session_state.projects_data = []
if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = None
if "interview_history" not in st.session_state:
    st.session_state.interview_history = []
if "assessment_scores" not in st.session_state:
    st.session_state.assessment_scores = {}
if "profile_stats" not in st.session_state:
    st.session_state.profile_stats = {}

# ============================================================================
# SIDEBAR - Profile Management
# ============================================================================
with st.sidebar:
    st.title("👤 Profile Manager")
    
    # Profile selection
    st.session_state.profiles = get_all_profiles()
    profile_options = ["Create New"] + st.session_state.profiles
    selected = st.selectbox("Select Profile", profile_options)
    
    if selected != "Create New":
        st.session_state.current_profile = selected
        profile_data = load_profile(selected)
        st.session_state.profile_config = profile_data
        st.session_state.profile_stats = get_profile_stats(selected)
    
    st.divider()
    
    # Profile actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Stats", key="view_stats", use_container_width=True):
            if st.session_state.current_profile:
                st.session_state.show_stats = True
    
    with col2:
        if st.button("💾 Export", key="export_profile", use_container_width=True):
            if st.session_state.current_profile:
                st.session_state.show_export = True
    
    with col3:
        if st.button("🗑️ Delete", key="delete_profile", use_container_width=True):
            if st.session_state.current_profile:
                delete_profile(st.session_state.current_profile)
                st.session_state.current_profile = None
                st.rerun()
    
    st.divider()
    
    # Configuration section
    st.subheader("⚙️ Configuration")
    career_field = st.text_input("Career Field", value=st.session_state.profile_config.get("career_field", ""))
    goal = st.text_area("Career Goal", value=st.session_state.profile_config.get("goal", ""), height=100)
    experience = st.selectbox(
        "Experience Level",
        ["Beginner", "Intermediate", "Advanced", "Expert"],
        index=["Beginner", "Intermediate", "Advanced", "Expert"].index(st.session_state.profile_config.get("experience", "Beginner"))
    )
    
    if st.button("💾 Save Configuration", use_container_width=True):
        if career_field and goal:
            profile_name = st.session_state.current_profile or f"{career_field}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            config_data = {
                "career_field": career_field,
                "goal": goal,
                "experience": experience,
                "created_at": datetime.now().isoformat()
            }
            save_profile(profile_name, config_data)
            st.session_state.current_profile = profile_name
            st.success(f"✅ Profile '{profile_name}' saved!")
            st.rerun()
        else:
            st.error("Please fill in all fields")

# ============================================================================
# MAIN CONTENT - Tabs
# ============================================================================
st.title("🚀 Career Assistant Platform v2.0")
st.markdown("Your personalized career development companion")

# Custom CSS for enhanced tab spacing and UI
st.markdown(
    """
    <style>
    .stTabs [data-baseweb="tab-list"] {
        margin-bottom: 32px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 24px 32px !important;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 12px;
        margin-right: 16px;
        background: #f7f7fa;
        color: #222;
        transition: background 0.2s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: #e0e0f7;
        color: #1a1a40;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #d1eaff;
        color: #0057b8;
        box-shadow: 0 2px 8px rgba(0,87,184,0.08);
    }
    .stAppViewContainer .stTitle {
        font-size: 2.5rem;
        color: #0057b8;
        font-weight: 700;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🗺️ Roadmap",
    "\n\n💬 Chat Mentor",
    "\n\n💡 Projects",
    "\n\n📄 Resume",
    "\n\n🎤 Interview",
    "\n\n📝 Assessment",
    "\n\n📊 Analytics"
])

# ============================================================================
# TAB 1 - ROADMAP
# ============================================================================
with tab1:
    st.header("Your Career Roadmap")
    
    if st.session_state.current_profile:
        career_field = st.session_state.profile_config.get("career_field", "")
        experience = st.session_state.profile_config.get("experience", "Beginner")
        
        if st.button("Generate Roadmap", key="generate_roadmap"):
            with st.spinner("Creating your personalized roadmap..."):
                prompt = get_roadmap_prompt(career_field, experience)
                roadmap = query_model(
                    "You are an expert career counselor. Create a detailed career roadmap.",
                    prompt,
                    max_tokens=2000
                )
                st.session_state.roadmap_data = roadmap
                save_roadmap(st.session_state.current_profile, roadmap)
        
        if st.session_state.roadmap_data:
            st.markdown(st.session_state.roadmap_data)
            st.divider()
            
            if st.button("📥 Save Roadmap to Profile"):
                save_roadmap(st.session_state.current_profile, st.session_state.roadmap_data)
                st.success("✅ Roadmap saved to your profile!")
    else:
        st.info("👉 Create or select a profile in the sidebar to generate your roadmap")

# ============================================================================
# TAB 2 - CHAT MENTOR
# ============================================================================
with tab2:
    st.header("Chat with Your Career Mentor")
    
    if st.session_state.current_profile:
        career_field = st.session_state.profile_config.get("career_field", "")
        goal = st.session_state.profile_config.get("goal", "")
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.chat_message("user").write(message["content"])
            else:
                st.chat_message("assistant").write(message["content"])
        
        # Chat input
        user_input = st.chat_input("Ask your career mentor a question...")
        
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.chat_message("user").write(user_input)
            
            with st.spinner("Thinking..."):
                prompt = get_chat_prompt(career_field, goal, user_input)
                response = query_model(
                    "You are an experienced career mentor providing personalized advice.",
                    prompt,
                    max_tokens=1000
                )
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.chat_message("assistant").write(response)
                save_interview_session(st.session_state.current_profile, {
                    "type": "chat",
                    "timestamp": datetime.now().isoformat(),
                    "messages": st.session_state.chat_history
                })
    else:
        st.info("👉 Create or select a profile in the sidebar to chat with your mentor")

# ============================================================================
# TAB 3 - PROJECTS
# ============================================================================
with tab3:
    st.header("Portfolio Projects")
    
    if st.session_state.current_profile:
        career_field = st.session_state.profile_config.get("career_field", "")
        experience = st.session_state.profile_config.get("experience", "Beginner")
        
        if st.button("Generate Project Ideas", key="generate_projects"):
            with st.spinner("Finding perfect projects for you..."):
                prompt = get_projects_prompt(career_field, experience)
                projects = query_model(
                    "You are a project advisor helping build a strong portfolio.",
                    prompt,
                    max_tokens=1500
                )
                st.session_state.projects_data = projects
        
        if st.session_state.projects_data:
            st.markdown(st.session_state.projects_data)
            st.divider()
            
            if st.button("📥 Save Projects to Profile"):
                from utils.storage import save_roadmap
                save_roadmap(st.session_state.current_profile, {
                    "type": "projects",
                    "data": st.session_state.projects_data
                })
                st.success("✅ Projects saved!")
    else:
        st.info("👉 Create or select a profile in the sidebar to get project ideas")

# ============================================================================
# TAB 4 - RESUME
# ============================================================================
with tab4:
    st.header("Resume Challenge & Analysis")
    
    if st.session_state.current_profile:
        st.subheader("📋 Upload & Analyze Your Resume")
        resume_text = st.text_area(
            "Paste your resume content here:",
            height=300,
            key="resume_input"
        )
        
        if st.button("Analyze Resume", key="analyze_resume"):
            if resume_text:
                with st.spinner("Analyzing your resume..."):
                    prompt = get_resume_prompt(resume_text)
                    analysis = query_model(
                        "You are an expert career coach analyzing resumes.",
                        prompt,
                        max_tokens=1500
                    )
                    st.session_state.resume_analysis = analysis
                    save_resume_analysis(st.session_state.current_profile, analysis)
        
        if st.session_state.resume_analysis:
            st.markdown(st.session_state.resume_analysis)
    else:
        st.info("👉 Create or select a profile in the sidebar to analyze your resume")

# ============================================================================
# TAB 5 - INTERVIEW
# ============================================================================
with tab5:
    st.header("🎤 Interview Preparation")
    
    if st.session_state.current_profile:
        col1, col2 = st.columns(2)
        
        with col1:
            interview_type = st.selectbox(
                "Select Interview Type",
                ["Behavioral", "Technical", "Case Study", "General"]
            )
        
        with col2:
            role = st.text_input("Target Role")
        
        if st.button("Start Interview Practice", key="start_interview"):
            if role:
                with st.spinner("Generating interview question..."):
                    prompt = get_interview_prompt(interview_type, role)
                    question = query_model(
                        "You are an experienced interviewer.",
                        prompt,
                        max_tokens=500
                    )
                    st.session_state.interview_history.append({
                        "type": interview_type,
                        "question": question,
                        "role": role
                    })
        
        if st.session_state.interview_history:
            st.subheader("Interview Questions")
            for i, item in enumerate(st.session_state.interview_history):
                st.write(f"**Q{i+1}:** {item['question']}")
                answer = st.text_area(f"Your answer for Q{i+1}:", key=f"answer_{i}")
                
                if answer:
                    with st.spinner("Evaluating your answer..."):
                        followup_prompt = get_followup_prompt(item['question'], answer)
                        feedback = query_model(
                            "Provide constructive feedback on this interview answer.",
                            followup_prompt,
                            max_tokens=500
                        )
                        st.write("**Feedback:**")
                        st.write(feedback)
            
            if st.button("💾 Save Interview Session"):
                save_interview_session(st.session_state.current_profile, {
                    "type": "interview",
                    "timestamp": datetime.now().isoformat(),
                    "practice": st.session_state.interview_history
                })
                st.success("✅ Interview session saved!")
    else:
        st.info("👉 Create or select a profile in the sidebar to practice interviews")

# ============================================================================
# TAB 6 - ASSESSMENT
# ============================================================================
with tab6:
    st.header("📝 Skill Assessment")
    
    st.markdown("Test your skills and track your progress across different competencies.")
    
    topics = get_available_topics()
    selected_topic = st.selectbox("Select Assessment Topic", topics)
    
    num_questions = st.slider("Number of Questions", 1, 10, 5)
    
    if st.button("Start Assessment"):
        assessment = get_assessment(selected_topic, num_questions)
        st.session_state.current_assessment = assessment
        st.session_state.assessment_answers = {}
    
    if hasattr(st.session_state, 'current_assessment'):
        assessment = st.session_state.current_assessment
        st.write(f"**Topic:** {selected_topic}")
        st.write(f"**Questions:** {num_questions}")
        st.divider()
        
        for i, q in enumerate(assessment['questions']):
            st.write(f"**Q{i+1}: {q['question']}**")
            options = [q['a'], q['b'], q['c'], q['d']]
            answer = st.radio(f"Answer for Q{i+1}:", options, key=f"q_{i}")
            st.session_state.assessment_answers[i] = answer
        
        if st.button("Submit Assessment"):
            score_data = calculate_score(
                st.session_state.assessment_answers,
                assessment['correct_answers']
            )
            percentage = score_data['percentage']
            skill_level = get_skill_level(percentage)
            
            st.session_state.assessment_scores[selected_topic] = {
                "percentage": percentage,
                "level": skill_level,
                "timestamp": datetime.now().isoformat()
            }
            
            st.success(f"✅ Assessment Complete!")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Score", f"{percentage}%")
            with col2:
                st.metric("Skill Level", skill_level)
            with col3:
                st.metric("Correct Answers", f"{score_data['correct']}/{num_questions}")
            
            if st.session_state.current_profile:
                save_profile(st.session_state.current_profile, {
                    **st.session_state.profile_config,
                    "assessment_scores": st.session_state.assessment_scores
                })

# ============================================================================
# TAB 7 - ANALYTICS
# ============================================================================
with tab7:
    st.header("📊 Analytics & Insights")
    
    if st.session_state.current_profile:
        st.subheader(f"Profile: {st.session_state.current_profile}")
        
        # Profile Information
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Career Field", st.session_state.profile_config.get("career_field", "N/A"))
        with col2:
            st.metric("Experience Level", st.session_state.profile_config.get("experience", "N/A"))
        with col3:
            st.metric("Assessments Taken", len(st.session_state.assessment_scores))
        with col4:
            st.metric("Chat Messages", len(st.session_state.chat_history))
        
        st.divider()
        
        # Engagement Score
        stats = st.session_state.profile_stats
        engagement_score = calculate_engagement_score(stats)
        
        st.markdown(f"### Engagement Score: {engagement_score}/100")
        st.progress(engagement_score / 100)
        
        st.divider()
        
        # Assessment Results
        if st.session_state.assessment_scores:
            st.subheader("Assessment Results")
            for topic, result in st.session_state.assessment_scores.items():
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(f"{topic}", f"{result['percentage']}%")
                with col2:
                    st.write(f"**Level:** {result['level']}")
                with col3:
                    st.write(f"**Date:** {result['timestamp'][:10]}")
        
        st.divider()
        
        # Export Options
        st.subheader("📥 Export & Reports")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Download TXT Report"):
                report = generate_text_report(st.session_state.current_profile, stats)
                st.download_button(
                    label="Download Report",
                    data=report,
                    file_name=f"{st.session_state.current_profile}_report.txt",
                    mime="text/plain"
                )
        
        with col2:
            if st.button("📊 Download CSV Export"):
                csv_data = generate_csv_export([st.session_state.current_profile])
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"{st.session_state.current_profile}_export.csv",
                    mime="text/csv"
                )
        
        with col3:
            if st.button("📋 Download JSON Export"):
                json_data = generate_json_export([st.session_state.current_profile])
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"{st.session_state.current_profile}_export.json",
                    mime="application/json"
                )
        
        st.divider()
        
        # System Statistics
        st.subheader("System Statistics")
        all_profiles = get_all_profiles()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Profiles", len(all_profiles))
        with col2:
            st.metric("Current Session Messages", len(st.session_state.chat_history))
        with col3:
            st.metric("Assessments in System", len(st.session_state.assessment_scores))
    else:
        st.info("👉 Create or select a profile in the sidebar to view analytics")

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.markdown("""
<div style='text-align: center; color: #888; font-size: 0.85em;'>
    <p>Career Assistant Platform v2.0 | Powered by AI | © 2026</p>
    <p>All your data is stored locally for privacy</p>
</div>
""", unsafe_allow_html=True)
