"""
modules/projects.py

Project Ideas Generator module — Streamlit UI + logic.
"""

import streamlit as st
from utils.model import query_model
from prompts.projects_prompt import PROJECTS_SYSTEM_PROMPT, get_projects_user_prompt


def render_projects():
    """Render the Project Ideas Generator page."""

    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="module-header">
        <span class="module-icon">💡</span>
        <div>
            <h2>Project Ideas Generator</h2>
            <p>Get 5 portfolio-worthy project ideas tailored to your skill level and target role.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Input Form ───────────────────────────────────────────────────────────
    with st.form("projects_form"):
        col1, col2 = st.columns(2)

        with col1:
            skill_level = st.selectbox(
                "📈 Your Skill Level",
                ["Beginner", "Intermediate", "Advanced"],
                help="Determines the complexity of project suggestions."
            )

        with col2:
            target_role = st.text_input(
                "🎯 Target Role / Domain",
                placeholder="e.g. ML Engineer, Frontend Developer, Data Analyst...",
                help="Projects will be tailored to this specific role."
            )

        submitted = st.form_submit_button(
            "💡 Generate Project Ideas",
            use_container_width=True,
            type="primary"
        )

    # ── Generation ───────────────────────────────────────────────────────────
    if submitted:
        if not target_role.strip():
            st.error("⚠️ Please enter your target role/domain.")
            return

        with st.spinner("🤖 Generating portfolio-worthy project ideas..."):
            user_prompt = get_projects_user_prompt(skill_level, target_role.strip())
            result = query_model(PROJECTS_SYSTEM_PROMPT, user_prompt)

        st.success("✅ Here are your project ideas!")
        st.markdown("---")
        st.markdown(result)

        # Download option
        st.download_button(
            label="📥 Download Project Ideas (Markdown)",
            data=result,
            file_name=f"project_ideas_{target_role.replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    else:
        # Tips when not yet submitted
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="info-card">
                <div class="info-card-icon">🏗️</div>
                <h4>Portfolio Impact</h4>
                <p>Projects are chosen to demonstrate real competence to interviewers and clients.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="info-card">
                <div class="info-card-icon">🛠️</div>
                <h4>Tool Recommendations</h4>
                <p>Each project includes specific tools and technologies — no vague suggestions.</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="info-card">
                <div class="info-card-icon">📊</div>
                <h4>5 Unique Ideas</h4>
                <p>Get 5 distinct projects with problem statements, datasets, and expected outcomes.</p>
            </div>
            """, unsafe_allow_html=True)
