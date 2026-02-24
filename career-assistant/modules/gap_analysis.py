"""
gap_analysis.py — Skill Gap Analysis Module
Analyze gaps between current skills and target role requirements.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from modules.chat import query_model


# Job role skill requirements database
ROLE_REQUIREMENTS = {
    "Software Engineering": {
        "Programming Languages": 9,
        "System Design": 8,
        "Problem Solving": 9,
        "Testing & Debugging": 8,
        "Version Control": 8,
        "Communication": 7,
        "Teamwork": 8,
    },
    "Data Science": {
        "Python": 9,
        "Statistics": 9,
        "Data Analysis": 9,
        "Machine Learning": 8,
        "SQL": 8,
        "Data Visualization": 8,
        "Communication": 7,
        "Domain Knowledge": 7,
    },
    "Product Management": {
        "Strategic Thinking": 9,
        "Communication": 9,
        "Data Analysis": 8,
        "User Research": 8,
        "Leadership": 8,
        "Business Acumen": 8,
        "Problem Solving": 8,
        "Stakeholder Management": 8,
    },
    "UX/UI Design": {
        "Design Tools": 9,
        "User Research": 8,
        "Wireframing": 8,
        "Visual Design": 9,
        "Prototyping": 8,
        "Communication": 8,
        "Problem Solving": 8,
        "Creative Thinking": 9,
    },
    "DevOps": {
        "Linux/Unix": 9,
        "Containerization (Docker)": 9,
        "Cloud Platforms": 9,
        "Scripting": 8,
        "CI/CD Pipelines": 9,
        "Monitoring & Logging": 8,
        "Infrastructure as Code": 8,
        "Security Awareness": 8,
    },
    "Cloud Architecture": {
        "AWS/Azure/GCP": 9,
        "Architecture Design": 9,
        "Networking": 8,
        "Security": 9,
        "Scalability": 8,
        "Cost Optimization": 8,
        "Problem Solving": 8,
        "Communication": 7,
    },
    "Machine Learning": {
        "Python": 9,
        "Mathematics": 9,
        "Machine Learning Algorithms": 9,
        "Deep Learning": 8,
        "Data Preprocessing": 8,
        "Model Evaluation": 8,
        "Problem Solving": 9,
        "Statistics": 9,
    },
    "Full Stack Web Dev": {
        "Frontend (React/Vue/Angular)": 8,
        "Backend (Node/Python/Java)": 8,
        "Databases": 8,
        "APIs & Integration": 8,
        "Version Control": 8,
        "Problem Solving": 8,
        "Communication": 7,
        "Testing": 7,
    },
    "Mobile Development": {
        "Mobile Framework (React Native/Flutter)": 9,
        "Programming Languages": 8,
        "UI/UX Principles": 8,
        "APIs & Backend": 8,
        "Testing": 7,
        "Performance Optimization": 8,
        "Problem Solving": 8,
        "Communication": 7,
    },
}


def get_role_requirements(role):
    """Get skill requirements for a specific role."""
    return ROLE_REQUIREMENTS.get(role, {})


def calculate_gaps(current_skills, target_role):
    """Calculate skill gaps between current and target."""
    required = get_role_requirements(target_role)
    
    gaps = {}
    for skill, required_level in required.items():
        current_level = current_skills.get(skill, 0)
        gap = required_level - current_level
        gaps[skill] = {
            "current": current_level,
            "required": required_level,
            "gap": gap,
            "percentage_complete": (current_level / required_level * 100) if required_level > 0 else 0
        }
    
    return gaps


def get_learning_resources(skill, gap_level):
    """Get learning resources for a skill."""
    resources = {
        "Programming Languages": [
            "LeetCode",
            "HackerRank",
            "Codecademy",
            "Free Code Camp",
        ],
        "System Design": [
            "System Design Interview Course",
            "Grokking System Design",
            "YouTube Tutorials",
        ],
        "Machine Learning": [
            "Andrew Ng's ML Course",
            "Fast.ai",
            "Kaggle Competitions",
        ],
        "Data Analysis": [
            "Excel/Google Sheets Tutorials",
            "SQL Tutorial",
            "Tableau/Power BI",
        ],
        "Communication": [
            "Toastmasters",
            "Public Speaking Courses",
            "Writing Workshops",
        ],
    }
    
    return resources.get(skill, ["Udemy", "Coursera", "LinkedIn Learning"])


def render_gap_analysis():
    """Render the skill gap analysis interface."""
    st.markdown("""
    <div class="module-header">
        <div class="module-icon">⚙️</div>
        <div>
            <h2>Skill Gap Analysis</h2>
            <p>Identify gaps between your current skills and target role requirements</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if user has a profile
    if not st.session_state.get("current_profile"):
        st.warning("⚠️ Please select or create a career profile first!")
        return
    
    profile = st.session_state.current_profile
    
    # Get current skills from assessment
    if "skill_assessment" not in profile:
        st.info("📌 Complete a skill assessment first to see your gaps!")
        return
    
    current_skills = profile["skill_assessment"].get("technical_skills", {})
    target_role = profile.get("career_field", "Software Engineering")
    
    # Calculate gaps
    gaps = calculate_gaps(current_skills, target_role)
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Gap Analysis", "🎯 Learning Plan", "📈 Progress"])
    
    with tab1:
        render_gap_overview(target_role, gaps)
    
    with tab2:
        render_learning_plan(gaps)
    
    with tab3:
        render_progress_tracking(profile, target_role, gaps)


def render_gap_overview(target_role, gaps):
    """Render gap analysis overview."""
    st.subheader(f"Gap Analysis for {target_role}")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_skills = len(gaps)
    mastered_skills = sum(1 for g in gaps.values() if g["gap"] <= 0)
    avg_gap = sum(g["gap"] for g in gaps.values()) / total_skills if total_skills > 0 else 0
    avg_completion = sum(g["percentage_complete"] for g in gaps.values()) / total_skills if total_skills > 0 else 0
    
    with col1:
        st.metric("Total Skills", total_skills)
    with col2:
        st.metric("Mastered", mastered_skills)
    with col3:
        st.metric("Avg Gap", f"{avg_gap:.1f}/10")
    with col4:
        st.metric("Avg Completion", f"{avg_completion:.0f}%")
    
    st.divider()
    
    # Radar chart of skills
    st.markdown("### 🎯 Skills Comparison")
    
    skills_list = list(gaps.keys())
    current_levels = [gaps[s]["current"] for s in skills_list]
    required_levels = [gaps[s]["required"] for s in skills_list]
    
    fig = go.Figure(data=[
        go.Scatterpolar(
            r=current_levels,
            theta=skills_list,
            fill='toself',
            name='Current Level'
        ),
        go.Scatterpolar(
            r=required_levels,
            theta=skills_list,
            fill='toself',
            name='Required Level'
        )
    ])
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True,
        height=600,
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Skills breakdown
    st.markdown("### 📋 Detailed Skill Breakdown")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        with st.expander("Critical Gaps (Need Immediate Work)", expanded=True):
            critical = {k: v for k, v in gaps.items() if v["gap"] > 3}
            if critical:
                for skill, gap_data in sorted(critical.items(), key=lambda x: x[1]["gap"], reverse=True):
                    col_a, col_b, col_c = st.columns([2, 1, 1])
                    with col_a:
                        st.progress(gap_data["percentage_complete"] / 100, text=skill)
                    with col_b:
                        st.caption(f"{gap_data['current']:.0f}/10")
                    with col_c:
                        st.metric("Gap", f"+{gap_data['gap']:.0f}", label_visibility="collapsed")
            else:
                st.success("✅ No critical gaps!")
        
        with st.expander("Medium Gaps (Good to Improve)"):
            medium = {k: v for k, v in gaps.items() if 1 < v["gap"] <= 3}
            if medium:
                for skill, gap_data in sorted(medium.items(), key=lambda x: x[1]["gap"], reverse=True):
                    col_a, col_b, col_c = st.columns([2, 1, 1])
                    with col_a:
                        st.progress(gap_data["percentage_complete"] / 100, text=skill)
                    with col_b:
                        st.caption(f"{gap_data['current']:.0f}/10")
                    with col_c:
                        st.metric("Gap", f"+{gap_data['gap']:.0f}", label_visibility="collapsed")
            else:
                st.info("No medium gaps")
        
        with st.expander("Small Gaps (Polish)"):
            small = {k: v for k, v in gaps.items() if 0 < v["gap"] <= 1}
            if small:
                for skill, gap_data in sorted(small.items(), key=lambda x: x[1]["gap"], reverse=True):
                    col_a, col_b, col_c = st.columns([2, 1, 1])
                    with col_a:
                        st.progress(gap_data["percentage_complete"] / 100, text=skill)
                    with col_b:
                        st.caption(f"{gap_data['current']:.0f}/10")
                    with col_c:
                        st.metric("Gap", f"+{gap_data['gap']:.1f}", label_visibility="collapsed")
            else:
                st.info("No small gaps")


def render_learning_plan(gaps):
    """Render personalized learning plan."""
    st.subheader("📚 Personalized Learning Plan")
    
    # Sort by gap size
    sorted_gaps = sorted(gaps.items(), key=lambda x: x[1]["gap"], reverse=True)
    
    st.markdown("""
    <div class="tips-box">
        <h4>🎯 Recommended Learning Order</h4>
        <p>Focus on critical gaps first (3+ points), then medium gaps, then polish remaining skills.</p>
    </div>
    """, unsafe_allow_html=True)
    
    for idx, (skill, gap_data) in enumerate(sorted_gaps, 1):
        if gap_data["gap"] > 0:
            with st.expander(f"{idx}. {skill} (Gap: +{gap_data['gap']:.0f}/10)", expanded=idx <= 2):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Estimate time to learn
                    hours_needed = gap_data["gap"] * 20  # Rough estimate
                    st.markdown(f"""
                    **Current Level:** {gap_data['current']:.0f}/10  
                    **Target Level:** {gap_data['required']:.0f}/10  
                    **Gap:** {gap_data['gap']:.0f} points  
                    **Est. Time:** ~{hours_needed:.0f} hours  
                    """)
                    
                with col2:
                    progress_pct = gap_data["percentage_complete"]
                    st.metric("Completion", f"{progress_pct:.0f}%")
                
                st.divider()
                
                # Learning resources
                st.markdown("**📖 Learning Resources:**")
                resources = get_learning_resources(skill, gap_data["gap"])
                for i, resource in enumerate(resources[:3], 1):
                    st.caption(f"{i}. {resource}")
                
                # Suggested milestones
                st.markdown("**🏆 Suggested Milestones:**")
                milestone_levels = [
                    (gap_data["current"] + (gap_data["gap"] / 3), "Level 1"),
                    (gap_data["current"] + (2 * gap_data["gap"] / 3), "Level 2"),
                    (gap_data["required"], "Mastery"),
                ]
                for level, label in milestone_levels:
                    st.caption(f"📌 {label}: {level:.0f}/10")


def render_progress_tracking(profile, target_role, gaps):
    """Render progress tracking toward skill goals."""
    st.subheader("📈 Your Progress Trajectory")
    
    # Initialize progress tracking if needed
    if "gap_progress_history" not in st.session_state:
        st.session_state.gap_progress_history = {
            "dates": [datetime.now().isoformat()],
            "avg_skills": [sum(g["current"] for g in gaps.values()) / len(gaps) if gaps else 0],
        }
    
    history = st.session_state.gap_progress_history
    
    # Show progress chart
    if len(history["dates"]) > 1:
        fig = px.line(
            x=history["dates"],
            y=history["avg_skills"],
            markers=True,
            title="Average Skill Level Over Time",
            labels={"x": "Date", "y": "Average Skill Level"},
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Estimate time to reach target
    st.markdown("### ⏱️ Timeline Projection")
    
    avg_current = sum(g["current"] for g in gaps.values()) / len(gaps) if gaps else 0
    avg_required = sum(g["required"] for g in gaps.values()) / len(gaps) if gaps else 0
    avg_gap = avg_required - avg_current
    
    if avg_gap > 0:
        weeks_to_goal = (avg_gap * 20) / 7  # Assuming 20 hours per skill level point
        months_to_goal = weeks_to_goal / 4
        
        st.metric("Estimated Time to Goal", f"{months_to_goal:.1f} months", f"({weeks_to_goal:.0f} weeks)")
        
        # Create timeline visualization
        timeline_data = {
            "Current": avg_current,
            "3 Months": min(avg_current + (avg_gap / 4), avg_required),
            "6 Months": min(avg_current + (avg_gap / 2), avg_required),
            "Target": avg_required,
        }
        
        fig = px.bar(
            x=list(timeline_data.keys()),
            y=list(timeline_data.values()),
            title="Projected Skill Growth",
            labels={"x": "Timeline", "y": "Average Skill Level"},
        )
        fig.add_hline(y=avg_required, line_dash="dash", line_color="green", annotation_text="Target")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("🎉 You're at or above the target level for all skills!")
