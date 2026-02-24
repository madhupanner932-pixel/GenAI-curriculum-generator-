"""
progress.py — Progress Tracking & Analytics Module
Track career development milestones and visualize progress.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from modules.chat import query_model
from prompts.skills_prompt import get_progress_tracking_prompt


def render_progress():
    """Render the progress tracking interface."""
    st.markdown("""
    <div class="module-header">
        <div class="module-icon">📊</div>
        <div>
            <h2>Progress & Analytics</h2>
            <p>Track your career development journey and visualize growth</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if user has a profile
    if "current_profile" not in st.session_state or not st.session_state.current_profile:
        st.warning("⚠️ Please select or create a career profile first!")
        return
    
    profile = st.session_state.current_profile
    
    # Initialize progress tracking in session state
    if "progress_data" not in st.session_state:
        st.session_state.progress_data = {
            "current_level": profile.get("experience_level", "Beginner"),
            "milestones": [],
            "completed_milestones": [],
            "in_progress": [],
            "skills_improved": [],
            "projects_completed": [],
            "created_date": datetime.now().isoformat()
        }
    
    # Tabs for different tracking views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Overview", 
        "✅ Milestones", 
        "📚 Skills Progress", 
        "🎯 Analytics"
    ])
    
    with tab1:
        render_progress_overview(profile)
    
    with tab2:
        render_milestones_tracker(profile)
    
    with tab3:
        render_skills_progress(profile)
    
    with tab4:
        render_analytics_dashboard(profile)


def render_progress_overview(profile):
    """Render progress overview section."""
    st.subheader("Your Journey 🚀")
    
    progress_data = st.session_state.progress_data
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        completed = len(progress_data["completed_milestones"])
        st.metric(
            "Completed",
            completed,
            help="Milestones completed"
        )
    
    with col2:
        in_prog = len(progress_data["in_progress"])
        st.metric(
            "In Progress",
            in_prog,
            help="Currently working on"
        )
    
    with col3:
        projects = len(progress_data["projects_completed"])
        st.metric(
            "Projects Built",
            projects,
            help="Portfolio projects completed"
        )
    
    with col4:
        skills = len(progress_data["skills_improved"])
        st.metric(
            "Skills Improved",
            skills,
            help="New skills acquired"
        )
    
    st.divider()
    
    # Progress tracking form
    st.markdown("### 📝 Log Your Progress")
    
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        progress_type = st.selectbox(
            "What did you accomplish?",
            ["Completed a milestone", "Started learning", "Finished a project", "Improved a skill"],
            key="progress_type"
        )
    
    with col_b:
        log_date = st.date_input("Date:", value=datetime.now().date())
    
    if progress_type == "Completed a milestone":
        milestone = st.text_input("Milestone description:", key="milestone_log")
        if st.button("✅ Log Milestone", use_container_width=True):
            progress_data["completed_milestones"].append({
                "title": milestone,
                "date": str(log_date)
            })
            # Save to profile
            profile["progress_data"] = progress_data
            st.session_state.profile_manager.update_profile(profile["name"], {"progress_data": progress_data})
            st.success(f"✨ Milestone '{milestone}' logged!")
            st.rerun()
    
    elif progress_type == "Started learning":
        skill = st.text_input("Skill you're learning:", key="skill_log")
        if st.button("📚 Log Learning", use_container_width=True):
            progress_data["in_progress"].append({
                "skill": skill,
                "start_date": str(log_date)
            })
            # Save to profile
            profile["progress_data"] = progress_data
            st.session_state.profile_manager.update_profile(profile["name"], {"progress_data": progress_data})
            st.success(f"🎯 Started learning '{skill}'!")
            st.rerun()
    
    elif progress_type == "Finished a project":
        project = st.text_input("Project name:", key="project_log")
        description = st.textarea("Project description:", key="project_desc")
        if st.button("🎉 Log Project", use_container_width=True):
            progress_data["projects_completed"].append({
                "name": project,
                "description": description,
                "date": str(log_date)
            })
            # Save to profile
            profile["progress_data"] = progress_data
            st.session_state.profile_manager.update_profile(profile["name"], {"progress_data": progress_data})
            st.success(f"🚀 Project '{project}' logged!")
            st.rerun()
    
    elif progress_type == "Improved a skill":
        skill_name = st.text_input("Skill improved:", key="skill_improved")
        improvement_level = st.slider("Improvement (1-10):", 1, 10, 5)
        if st.button("⬆️ Log Improvement", use_container_width=True):
            progress_data["skills_improved"].append({
                "skill": skill_name,
                "level": improvement_level,
                "date": str(log_date)
            })
            # Save to profile
            profile["progress_data"] = progress_data
            st.session_state.profile_manager.update_profile(profile["name"], {"progress_data": progress_data})
            st.success(f"📈 Improvement in '{skill_name}' logged!")
            st.rerun()
    
    st.divider()
    
    # Recent activity
    st.markdown("### 📋 Recent Activity")
    
    all_activities = [
        ("✅", f"Completed: {m['title']}", m['date']) 
        for m in progress_data["completed_milestones"][-3:]
    ] + [
        ("📚", f"Learning: {s['skill']}", s['start_date']) 
        for s in progress_data["in_progress"][-2:]
    ]
    
    if all_activities:
        activity_df = pd.DataFrame(all_activities, columns=["Type", "Activity", "Date"])
        st.dataframe(activity_df, use_container_width=True, hide_index=True)
    else:
        st.info("No activities logged yet. Start tracking your progress!")


def render_milestones_tracker(profile):
    """Render milestones tracking section."""
    st.subheader("🏆 Milestone Tracker")
    
    progress_data = st.session_state.progress_data
    career_field = profile.get("career_field", "")
    
    # Get milestones from roadmap if available
    if "roadmap_data" in st.session_state:
        roadmap = st.session_state.roadmap_data
        milestones = roadmap.get("milestones", [])
    else:
        milestones = ["Phase 1: Fundamentals", "Phase 2: Core Skills", "Phase 3: Advanced Topics", "Phase 4: Specialization"]
    
    st.info("Mark milestones as you progress through your career path")
    
    # Interactive milestone tracker
    for i, milestone in enumerate(milestones):
        col1, col2, col3 = st.columns([0.5, 2, 0.5])
        
        is_completed = milestone in [m.get("title") for m in progress_data["completed_milestones"]]
        is_in_progress = milestone in [s.get("skill") for s in progress_data["in_progress"]]
        
        with col1:
            if is_completed:
                st.markdown("✅")
            elif is_in_progress:
                st.markdown("⏳")
            else:
                st.markdown("📌")
        
        with col2:
            st.write(milestone)
        
        with col3:
            if not is_completed:
                if st.button("Mark Done", key=f"mark_{i}"):
                    progress_data["completed_milestones"].append({
                        "title": milestone,
                        "date": datetime.now().strftime("%Y-%m-%d")
                    })
                    st.success("✅ Milestone completed!")
                    st.rerun()
    
    st.divider()
    
    # Milestone timeline visualization
    if progress_data["completed_milestones"]:
        st.markdown("#### Completion Timeline")
        
        completion_data = []
        for m in progress_data["completed_milestones"]:
            completion_data.append({
                "Milestone": m["title"],
                "Date": pd.to_datetime(m["date"])
            })
        
        if completion_data:
            df = pd.DataFrame(completion_data)
            fig = px.bar(df, x="Date", y="Milestone", orientation="h", 
                        title="Milestone Completion Timeline",
                        color_discrete_sequence=["#6C63FF"])
            fig.update_layout(
                template="plotly_dark",
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)


def render_skills_progress(profile):
    """Render skills progress section."""
    st.subheader("📈 Skills Development")
    
    progress_data = st.session_state.progress_data
    
    if progress_data["skills_improved"]:
        # Skills improvement chart
        skills_df = pd.DataFrame(progress_data["skills_improved"])
        
        fig = px.bar(
            skills_df,
            x="skill",
            y="level",
            title="Skills Improvement Levels",
            color="level",
            color_continuous_scale=["#FF6584", "#43E97B"],
            range_color=[1, 10]
        )
        fig.update_layout(
            template="plotly_dark",
            height=400,
            xaxis_title="Skill",
            yaxis_title="Proficiency Level (1-10)"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Skills table
        st.markdown("#### Skills Breakdown")
        st.dataframe(skills_df, use_container_width=True, hide_index=True)
    
    else:
        st.info("Log your skill improvements to see progress here")


def render_analytics_dashboard(profile):
    """Render comprehensive analytics dashboard."""
    st.subheader("📊 Career Analytics")
    
    progress_data = st.session_state.progress_data
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Completion rate
        completed = len(progress_data["completed_milestones"])
        total = max(1, completed + len(progress_data["in_progress"]) + 5)
        completion_rate = (completed / total) * 100
        
        fig = go.Figure(data=[go.Pie(
            labels=["Completed", "In Progress", "Remaining"],
            values=[completed, len(progress_data["in_progress"]), total - completed],
            hole=0.3,
            marker=dict(colors=["#43E97B", "#6C63FF", "#FF6584"])
        )])
        fig.update_layout(
            template="plotly_dark",
            title="Progress Completion Rate",
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Projects & activities
        st.markdown("#### 🎯 Activity Summary")
        st.metric("Total Projects", len(progress_data["projects_completed"]))
        st.metric("Active Learning", len(progress_data["in_progress"]))
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    st.divider()
    
    # Get AI motivation and guidance
    if st.button("🤖 Get Progress Insights", key="progress_insights"):
        with st.spinner("Analyzing your progress..."):
            try:
                prompt = get_progress_tracking_prompt(
                    career_field=profile.get("career_field", ""),
                    milestones=[m.get("title") for m in progress_data["completed_milestones"]],
                    completed=progress_data["completed_milestones"],
                    in_progress=progress_data["in_progress"]
                )
                
                response = query_model(prompt)
                st.markdown("### 💡 Your Progress Insights")
                st.markdown(response)
                
            except Exception as e:
                st.error(f"Error getting insights: {str(e)}")
