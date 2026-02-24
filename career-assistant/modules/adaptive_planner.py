"""
adaptive_planner.py — Smart Weekly Adaptive Planner
Adjusts roadmap based on user progress, burnout warnings, and velocity.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import json


def calculate_completion_velocity(progress_history):
    """Calculate user's learning velocity."""
    if len(progress_history) < 2:
        return 1.0
    
    recent = progress_history[-7:]  # Last 7 days
    completed = sum(1 for p in recent if p.get("completed", False))
    planned = len(recent)
    
    if planned == 0:
        return 1.0
    
    return completed / planned


def generate_adaptive_plan(profile, roadmap_weeks, base_tasks):
    """Generate adaptive weekly plan."""
    if "completion_history" not in st.session_state:
        st.session_state.completion_history = []
    
    velocity = calculate_completion_velocity(st.session_state.completion_history)
    
    # Adjust plan based on velocity
    if velocity < 0.5 and len(st.session_state.completion_history) > 5:
        adjustment = "slower"
        weeks_adjusted = roadmap_weeks * 1.5  # Extend timeline
        daily_tasks = max(1, base_tasks - 1)
    elif velocity > 0.9:
        adjustment = "faster"
        weeks_adjusted = roadmap_weeks * 0.7  # Compress timeline
        daily_tasks = base_tasks + 1
    else:
        adjustment = "on_track"
        weeks_adjusted = roadmap_weeks
        daily_tasks = base_tasks
    
    return {
        "adjustment": adjustment,
        "weeks": weeks_adjusted,
        "daily_tasks": daily_tasks,
        "velocity": velocity,
    }


def render_adaptive_planner():
    """Render smart adaptive weekly planner."""
    st.markdown("""
    <div class="module-header">
        <div class="module-icon">📅</div>
        <div>
            <h2>Smart Adaptive Weekly Planner</h2>
            <p>Auto-adjusts based on your progress, prevents burnout</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.get("current_profile"):
        st.warning("⚠️ Please select or create a profile first!")
        return
    
    profile = st.session_state.current_profile
    
    # Initialize completion history
    if "completion_history" not in st.session_state:
        st.session_state.completion_history = [
            {"date": datetime.now().isoformat(), "completed": True, "tasks": 2}
            for _ in range(7)
        ]
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Weekly Plan", "📈 Progress Velocity", "⚠️ Burnout Check", "📊 Analytics"])
    
    with tab1:
        st.subheader("Your Adaptive Weekly Plan")
        
        # Get plan parameters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            roadmap_weeks = st.slider("Roadmap duration (weeks):", 8, 52, 24)
        
        with col2:
            base_tasks = st.slider("Daily tasks target:", 1, 5, 3)
        
        with col3:
            st.metric("Your Velocity", f"{calculate_completion_velocity(st.session_state.completion_history)*100:.0f}%")
        
        # Generate adaptive plan
        plan = generate_adaptive_plan(profile, roadmap_weeks, base_tasks)
        
        st.divider()
        
        # Display plan adjustments
        if plan["adjustment"] == "faster":
            st.success(f"🚀 You're progressing fast! Timeline compressed to {plan['weeks']:.0f} weeks")
            st.info(f"Suggested daily tasks: {plan['daily_tasks']} (increased from {base_tasks})")
        elif plan["adjustment"] == "slower":
            st.warning(f"⏱️ Adjusting pace. Extended timeline to {plan['weeks']:.0f} weeks")
            st.info(f"Suggested daily tasks: {plan['daily_tasks']} (reduced to prevent burnout)")
        else:
            st.info(f"✅ You're on track! Maintaining {plan['daily_tasks']} daily tasks over {plan['weeks']:.0f} weeks")
        
        st.divider()
        
        # Weekly breakdown
        st.markdown("### 📅 This Week's Learning Plan")
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Sample learning topics
        learning_topics = [
            "Core Concepts",
            "Hands-on Practice",
            "Project Work",
            "Review & Quiz",
            "Advanced Topics",
            "Mini-Project",
            "Rest & Reflection"
        ]
        
        week_plan = pd.DataFrame({
            "Day": days,
            "Topic": learning_topics,
            "Duration": ["2h", "2h", "2h", "2h", "3h", "4h", "1h"],
            "Status": ["Planned"] * 7,
        })
        
        st.dataframe(week_plan, use_container_width=True, hide_index=True)
        
        # Mark completions
        st.divider()
        st.markdown("### ✅ Today's Progress")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tasks_done = st.slider("Tasks completed today:", 0, plan['daily_tasks'], 0)
        
        with col2:
            if st.button("✅ Log Today"):
                new_entry = {
                    "date": datetime.now().isoformat(),
                    "completed": tasks_done >= plan['daily_tasks'],
                    "tasks": tasks_done,
                }
                st.session_state.completion_history.append(new_entry)
                st.success("✅ Progress logged!")
                st.rerun()
        
        with col3:
            pass
    
    with tab2:
        st.subheader("📈 Your Learning Velocity")
        
        # Create velocity history
        history_dates = [
            datetime.now() - timedelta(days=6-i) 
            for i in range(len(st.session_state.completion_history))
        ]
        
        velocity_df = pd.DataFrame({
            "Date": [h.strftime("%a") for h in history_dates],
            "Completed": [1 if h.get("completed", False) else 0 for h in st.session_state.completion_history],
        })
        
        # Velocity chart
        fig = go.Figure(data=[
            go.Bar(
                x=velocity_df["Date"],
                y=velocity_df["Completed"],
                marker_color=["#43E97B" if c else "#FF6584" for c in velocity_df["Completed"]],
                text=["Complete" if c else "Incomplete" for c in velocity_df["Completed"]],
                textposition="auto",
            )
        ])
        fig.update_layout(
            title="7-Day Completion Rate",
            yaxis_title="Status",
            height=400,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Velocity insights
        velocity = calculate_completion_velocity(st.session_state.completion_history)
        
        st.markdown("### 📊 Velocity Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Current Velocity", f"{velocity*100:.0f}%")
        
        with col2:
            recent_days = sum(1 for h in st.session_state.completion_history[-7:] if h.get("completed"))
            st.metric("Last 7 Days", f"{recent_days}/7 completed")
        
        with col3:
            predicted_weeks = 24 / (velocity if velocity > 0 else 0.5)
            st.metric("Est. Completion", f"{predicted_weeks:.0f} weeks")
    
    with tab3:
        st.subheader("⚠️ Burnout Prevention")
        
        velocity = calculate_completion_velocity(st.session_state.completion_history)
        
        # Burnout risk assessment
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔥 Burnout Risk Assessment")
            
            if velocity < 0.5:
                st.error("❌ HIGH RISK - You're overextended!")
                st.write("""
                **Recommendations:**
                - Reduce daily tasks to 2
                - Add 1 rest day per week
                - Take a3-day break after 3 weeks
                """)
            elif velocity < 0.7:
                st.warning("⚠️ MODERATE RISK - Adjust pace")
                st.write("""
                **Recommendations:**
                - Reduce tasks slightly
                - Ensure 2 rest days/week
                - Monitor stress levels
                """)
            else:
                st.success("✅ HEALTHY - You're sustainable!")
                st.write("""
                **Keep it up:**
                - Maintain current pace
                - Rest properly on weekends
                - Celebrate wins
                """)
        
        with col2:
            st.markdown("### 📋 Wellness Checklist")
            
            col_a, col_b = st.columns([3, 1])
            
            wellness_items = [
                ("✅ Sleep 7+ hours", True),
                ("💧 Drink water regularly", True),
                ("🏃 Exercise 30 min/day", True),
                ("😊 Take breaks every hour", False),
                ("🧘 Meditate/stretch", False),
            ]
            
            for item, default in wellness_items:
                done = st.checkbox(item, value=default)
        
        st.divider()
        
        # Break recommendations
        st.markdown("### 🏖️ Recommended Breaks")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Daily:** 15 min break every 90 min")
        
        with col2:
            st.markdown("**Weekly:** 1 full rest day")
        
        with col3:
            st.markdown("**Monthly:** 3-day long weekend")
    
    with tab4:
        st.subheader("📊 Learning Analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_days = len(st.session_state.completion_history)
            completed_days = sum(1 for h in st.session_state.completion_history if h.get("completed"))
            st.metric("Completion Rate", f"{completed_days}/{total_days}")
        
        with col2:
            total_tasks = sum(h.get("tasks", 0) for h in st.session_state.completion_history)
            st.metric("Total Tasks", total_tasks)
        
        with col3:
            avg_tasks = total_tasks / max(total_days, 1)
            st.metric("Avg/Day", f"{avg_tasks:.1f}")
        
        with col4:
            velocity = calculate_completion_velocity(st.session_state.completion_history)
            st.metric("Velocity", f"{velocity*100:.0f}%")
        
        st.divider()
        
        # Trend analysis
        st.markdown("### 📈 Trend Analysis")
        
        trend_df = pd.DataFrame({
            "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
            "Completion %": [75, 72, 85, 88],
            "Tasks Done": [15, 14, 17, 18],
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=trend_df["Week"],
            y=trend_df["Completion %"],
            name="Completion %",
            yaxis="y",
            marker=dict(color="#6C63FF"),
        ))
        
        fig.add_trace(go.Scatter(
            x=trend_df["Week"],
            y=trend_df["Tasks Done"],
            name="Tasks Done",
            yaxis="y2",
            marker=dict(color="#FF6584"),
        ))
        
        fig.update_layout(
            yaxis=dict(title="Completion %"),
            yaxis2=dict(title="Tasks Done", overlaying="y", side="right"),
            title="4-Week Trend Analysis",
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)
