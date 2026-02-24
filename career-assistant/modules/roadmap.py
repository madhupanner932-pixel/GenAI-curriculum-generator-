"""
modules/roadmap.py

Career Roadmap Generator module — Streamlit UI + logic.
"""

import streamlit as st
from utils.model import query_model
from prompts.roadmap_prompt import ROADMAP_SYSTEM_PROMPT, get_roadmap_user_prompt


def render_roadmap():
    """Render the Career Roadmap Generator page."""

    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="module-header">
        <span class="module-icon">🗺️</span>
        <div>
            <h2>Career Roadmap Generator</h2>
            <p>Get a personalized, step-by-step career plan tailored to your goals and schedule.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Get profile data if available
    profile = st.session_state.get("current_profile")
    default_level = profile.get("experience_level", "Intermediate") if profile else "Intermediate"
    default_field = profile.get("career_field", "") if profile else ""

    # ── Input Form ───────────────────────────────────────────────────────────
    with st.form("roadmap_form"):
        col1, col2 = st.columns(2)

        with col1:
            skill_level = st.selectbox(
                "📈 Current Skill Level",
                ["Beginner", "Intermediate", "Advanced"],
                index=["Beginner", "Intermediate", "Advanced"].index(default_level) if default_level in ["Beginner", "Intermediate", "Advanced"] else 1,
                help="Be honest — this ensures realistic milestones."
            )
            target_role = st.text_input(
                "🎯 Target Role / Field",
                value=default_field,
                placeholder="e.g. Data Scientist, Full Stack Developer, UX Designer...",
                help="Be as specific as possible for a better roadmap."
            )

        with col2:
            daily_hours = st.slider(
                "⏰ Daily Time Available (hours)",
                min_value=0.5, max_value=12.0, value=2.0, step=0.5,
                help="Realistic time you can commit daily."
            )
            timeline = st.selectbox(
                "📅 Target Timeline",
                ["3 months", "6 months", "12 months", "18 months"],
                index=1,
                help="How long you want to reach your goal."
            )

        submitted = st.form_submit_button(
            "🚀 Generate My Roadmap",
            use_container_width=True,
            type="primary"
        )

    # ── Generation ───────────────────────────────────────────────────────────
    if submitted:
        if not target_role.strip():
            st.error("⚠️ Please enter your target role/field.")
            return

        with st.spinner("🤖 Crafting your personalized career roadmap..."):
            user_prompt = get_roadmap_user_prompt(
                skill_level, target_role.strip(), str(daily_hours), timeline
            )
            result = query_model(ROADMAP_SYSTEM_PROMPT, user_prompt)

        # Display result
        st.success("✅ Your roadmap is ready!")
        st.markdown("---")
        st.markdown(result)

        # Save to profile if available
        if profile:
            if st.button("💾 Save This Roadmap to Profile"):
                profile["roadmap_data"] = {
                    "target_role": target_role.strip(),
                    "skill_level": skill_level,
                    "daily_hours": daily_hours,
                    "timeline": timeline,
                    "roadmap": result,
                    "created_at": st.session_state.profile_manager.load_profile(profile["name"]).get("updated_at", "")
                }
                st.session_state.profile_manager.update_profile(profile["name"], {"roadmap_data": profile["roadmap_data"]})
                st.success("✅ Roadmap saved to profile!")

        # Download option
        st.download_button(
            label="📥 Download Roadmap (Markdown)",
            data=result,
            file_name=f"career_roadmap_{target_role.replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    else:
        # Show tips when not yet submitted
        st.markdown("""
        <div class="tips-box">
            <h4>💡 How to get the best roadmap</h4>
            <ul>
                <li><strong>Be specific</strong> with your target role (e.g., "ML Engineer at a startup")</li>
                <li><strong>Be honest</strong> about your skill level and available time</li>
                <li><strong>Commit</strong> to a realistic timeline — quality over speed</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if profile:
            st.info(f"👤 Using profile: **{profile['name']}** ({profile.get('career_field', 'N/A')})")
