"""
modules/user_history.py

User Activity History & Analytics Dashboard
Tracks daily usage patterns, feature access, and engagement metrics
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from collections import Counter
import json

# Feature emoji mapping
FEATURE_EMOJI = {
    "Resume Gap Analyzer": "📄",
    "Market Trends": "📊",
    "Adaptive Planner": "🗓️",
    "Chat": "💬",
    "Skills": "🎯",
    "Roadmap": "🗺️",
    "Projects": "💻",
    "Interview Practice": "🎤",
    "Profile": "👤",
    "Resume": "📋",
    "Reports": "📈",
    "Gamification": "🎮",
}


def log_activity(profile, feature_name: str, duration_minutes: int = 5):
    """Log user activity to profile"""
    if not profile:
        return
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Initialize history if not exists
    if "activity_history" not in profile:
        profile["activity_history"] = []
    
    # Add activity entry
    activity_entry = {
        "date": today,
        "timestamp": datetime.now().isoformat(),
        "feature": feature_name,
        "duration_minutes": duration_minutes,
    }
    
    profile["activity_history"].append(activity_entry)
    
    # Keep only last 90 days
    cutoff_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    profile["activity_history"] = [
        a for a in profile["activity_history"] if a["date"] >= cutoff_date
    ]


def get_daily_summary(activity_history: list) -> dict:
    """Get today's activity summary"""
    today = datetime.now().strftime("%Y-%m-%d")
    today_activities = [a for a in activity_history if a["date"] == today]
    
    return {
        "total_features_accessed": len(set(a["feature"] for a in today_activities)),
        "total_time_minutes": sum(a["duration_minutes"] for a in today_activities),
        "features_list": [a["feature"] for a in today_activities],
        "activity_count": len(today_activities),
    }


def get_weekly_stats(activity_history: list) -> dict:
    """Get week's activity stats"""
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    week_activities = [
        a for a in activity_history 
        if datetime.fromisoformat(a["timestamp"]) >= datetime.fromisoformat(week_ago + "T00:00:00")
    ]
    
    # Daily breakdown
    daily_data = {}
    for activity in week_activities:
        date = activity["date"]
        daily_data[date] = daily_data.get(date, 0) + activity["duration_minutes"]
    
    # Feature usage count
    feature_usage = Counter([a["feature"] for a in week_activities])
    
    return {
        "daily_breakdown": daily_data,
        "feature_usage": dict(feature_usage),
        "total_activities": len(week_activities),
        "unique_days": len(set(a["date"] for a in week_activities)),
    }


def get_monthly_streak(activity_history: list) -> dict:
    """Calculate user's login/activity streak"""
    if not activity_history:
        return {"current_streak": 0, "longest_streak": 0}
    
    dates = sorted(set(a["date"] for a in activity_history))
    
    if not dates:
        return {"current_streak": 0, "longest_streak": 0}
    
    # Calculate current streak
    current_streak = 0
    today = datetime.now().date()
    check_date = today
    
    for date_str in reversed(dates):
        activity_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if (check_date - activity_date).days <= 1:
            current_streak += 1
            check_date = activity_date
        else:
            break
    
    # Calculate longest streak
    longest_streak = 1
    temp_streak = 1
    for i in range(1, len(dates)):
        date1 = datetime.strptime(dates[i-1], "%Y-%m-%d").date()
        date2 = datetime.strptime(dates[i], "%Y-%m-%d").date()
        
        if (date2 - date1).days == 1:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 1
    
    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "total_active_days": len(dates),
    }


def render_user_history():
    """Main user history dashboard"""
    
    # ─── Get/Initialize Current Profile ──────────────────────────────────
    if "profile_manager" not in st.session_state or not st.session_state.current_profile:
        st.warning("⚠️ Please select or create a profile first!")
        return
    
    profile = st.session_state.current_profile
    activity_history = profile.get("activity_history", [])
    language = st.session_state.get("language", "en")
    
    # ─── Main UI ─────────────────────────────────────────────────────────
    st.title("📊 User Activity History")
    
    if not activity_history:
        st.info("🎯 No activity recorded yet. Start using features to build your history!")
        return
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📅 Daily Summary", "📈 Weekly Stats", "🔥 Streaks", "📑 Full History"]
    )
    
    # ─── TAB 1: Daily Summary ─────────────────────────────────────────────
    with tab1:
        daily_summary = get_daily_summary(activity_history)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🎯 Features Today",
                daily_summary["total_features_accessed"],
                delta="visited" if daily_summary["total_features_accessed"] > 0 else "none"
            )
        
        with col2:
            st.metric(
                "⏱️ Time Spent (mins)",
                daily_summary["total_time_minutes"],
                delta=f"{daily_summary['activity_count']} activities"
            )
        
        with col3:
            hours = daily_summary["total_time_minutes"] / 60
            st.metric(
                "🕒 Hours Equivalent",
                f"{hours:.1f}h",
                delta="today"
            )
        
        with col4:
            st.metric(
                "📌 Last Updated",
                datetime.now().strftime("%H:%M"),
                delta="now"
            )
        
        st.divider()
        
        # Today's features
        if daily_summary["features_list"]:
            st.subheader("✨ Features Used Today")
            
            feature_counts = Counter(daily_summary["features_list"])
            today_df = pd.DataFrame([
                {
                    "Feature": f"{FEATURE_EMOJI.get(f, '📌')} {f}",
                    "Times Accessed": count,
                }
                for f, count in sorted(feature_counts.items(), key=lambda x: x[1], reverse=True)
            ])
            
            st.dataframe(today_df, use_container_width=True, hide_index=True)
    
    # ─── TAB 2: Weekly Stats ──────────────────────────────────────────────
    with tab2:
        weekly_stats = get_weekly_stats(activity_history)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "📊 Total Activities",
                weekly_stats["total_activities"],
                delta=f"{weekly_stats['unique_days']} days active"
            )
        
        with col2:
            avg_activity = weekly_stats["total_activities"] / max(1, weekly_stats["unique_days"])
            st.metric(
                "📈 Avg. per Day",
                f"{avg_activity:.1f}",
                delta="activities"
            )
        
        with col3:
            st.metric(
                "📅 Active Days",
                weekly_stats["unique_days"],
                delta="out of 7 days"
            )
        
        st.divider()
        
        # Daily breakdown chart
        if weekly_stats["daily_breakdown"]:
            st.subheader("📅 Daily Time Spent (Last 7 Days)")
            
            dates = sorted(weekly_stats["daily_breakdown"].keys())
            minutes = [weekly_stats["daily_breakdown"][d] for d in dates]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=dates,
                    y=minutes,
                    marker=dict(
                        color=minutes,
                        colorscale="Viridis",
                        showscale=True,
                        colorbar=dict(title="Minutes")
                    ),
                    text=[f"{m}m" for m in minutes],
                    textposition="auto",
                    hovertemplate="<b>%{x}</b><br>Time: %{y} minutes<extra></extra>"
                )
            ])
            
            fig.update_layout(
                title="Time Investment Over the Week",
                xaxis_title="Date",
                yaxis_title="Minutes Spent",
                height=400,
                showlegend=False,
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Feature usage pie chart
        if weekly_stats["feature_usage"]:
            st.subheader("🎯 Most Used Features")
            
            features = list(weekly_stats["feature_usage"].keys())
            counts = list(weekly_stats["feature_usage"].values())
            
            fig = px.pie(
                values=counts,
                names=[f"{FEATURE_EMOJI.get(f, '📌')} {f}" for f in features],
                title="Weekly Feature Distribution",
                hole=0.4,
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # ─── TAB 3: Streaks & Milestones ──────────────────────────────────────
    with tab3:
        streak_data = get_monthly_streak(activity_history)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "🔥 Current Streak",
                f"{streak_data['current_streak']} days",
                delta="Keep it going!" if streak_data['current_streak'] > 0 else "Start today!"
            )
        
        with col2:
            st.metric(
                "⭐ Longest Streak",
                f"{streak_data['longest_streak']} days",
                delta="best record"
            )
        
        with col3:
            st.metric(
                "📊 Total Active Days",
                streak_data["total_active_days"],
                delta="all time"
            )
        
        st.divider()
        
        # Streak visualization
        st.subheader("🗓️ Activity Calendar")
        
        # Create a 30-day calendar heatmap
        dates = sorted(set(a["date"] for a in activity_history))
        date_activity = {}
        
        for date_str in dates:
            activities = [a for a in activity_history if a["date"] == date_str]
            total_minutes = sum(a["duration_minutes"] for a in activities)
            date_activity[date_str] = total_minutes
        
        # Get last 30 days
        last_30_days = []
        today = datetime.now().date()
        for i in range(29, -1, -1):
            date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            last_30_days.append({
                "date": date,
                "minutes": date_activity.get(date, 0),
                "week": (datetime.strptime(date, "%Y-%m-%d").date().weekday()),
                "day": (datetime.strptime(date, "%Y-%m-%d").date().day),
            })
        
        # Create heatmap
        week_groups = {}
        for item in last_30_days:
            week_start = datetime.strptime(item["date"], "%Y-%m-%d").date() - timedelta(days=item["week"])
            week_key = week_start.strftime("%Y-W%U")
            if week_key not in week_groups:
                week_groups[week_key] = []
            week_groups[week_key].append(item)
        
        days_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        
        # Heatmap visualization
        heatmap_data = []
        for week_key in sorted(week_groups.keys()):
            week_data = week_groups[week_key]
            for i in range(7):
                matching = [d for d in week_data if d["week"] == i]
                if matching:
                    heatmap_data.append(matching[0]["minutes"])
                else:
                    heatmap_data.append(0)
        
        # Create mini calendar
        col_days = st.columns(7)
        for i, day_label in enumerate(days_labels):
            with col_days[i]:
                st.write(f"**{day_label}**")
        
        # Display activity as color blocks
        for idx, item in enumerate(last_30_days):
            if idx % 7 == 0:
                cols = st.columns(7)
            
            col_idx = idx % 7
            with cols[col_idx]:
                minutes = item["minutes"]
                if minutes == 0:
                    color = "⬜"
                elif minutes < 10:
                    color = "🟩"
                elif minutes < 30:
                    color = "🟩"
                elif minutes < 60:
                    color = "🟩"
                else:
                    color = "🟩"
                
                status = f"{color} {minutes}m" if minutes > 0 else f"{color}"
                st.write(status)
    
    # ─── TAB 4: Full History ──────────────────────────────────────────────
    with tab4:
        st.subheader("📑 Complete Activity Log")
        
        # Sort by date descending
        sorted_history = sorted(
            activity_history,
            key=lambda x: x["timestamp"],
            reverse=True
        )
        
        # Create dataframe
        history_df = pd.DataFrame([
            {
                "Date": a["date"],
                "Time": datetime.fromisoformat(a["timestamp"]).strftime("%H:%M"),
                "Feature": f"{FEATURE_EMOJI.get(a['feature'], '📌')} {a['feature']}",
                "Duration (min)": a["duration_minutes"],
            }
            for a in sorted_history
        ])
        
        # Display
        st.dataframe(history_df, use_container_width=True, hide_index=True)
        
        # Export button
        csv = history_df.to_csv(index=False)
        st.download_button(
            label="📥 Download History as CSV",
            data=csv,
            file_name=f"activity_history_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
