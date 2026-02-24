"""
gamification.py — Gamification & Achievements System
Track achievements, earn badges, and maintain streaks.
"""

import streamlit as st
from datetime import datetime, timedelta
from utils.translations import get_text


# Achievement definitions
ACHIEVEMENTS = {
    "first_step": {
        "name": "Getting Started",
        "description": "Create your first career profile",
        "emoji": "🌱",
        "points": 10,
        "condition": lambda profile: profile is not None,
    },
    "skill_assessor": {
        "name": "Skill Assessor",
        "description": "Complete your first skill assessment",
        "emoji": "🎯",
        "points": 25,
        "condition": lambda profile: profile and "skill_assessment" in profile and len(profile.get("skill_assessment", {})) > 0,
    },
    "roadmap_builder": {
        "name": "Roadmap Builder",
        "description": "Create your first career roadmap",
        "emoji": "🗺️",
        "points": 30,
        "condition": lambda profile: profile and "roadmap_data" in profile,
    },
    "progress_tracker": {
        "name": "Progress Tracker",
        "description": "Log your first milestone in progress tracking",
        "emoji": "📊",
        "points": 20,
        "condition": lambda profile: profile and "progress_data" in profile and len(profile.get("progress_data", {}).get("completed_milestones", [])) > 0,
    },
    "mentor_seeker": {
        "name": "Mentor Seeker",
        "description": "Have 10 conversations with the AI mentor",
        "emoji": "💬",
        "points": 50,
        "condition": lambda msgs: len(st.session_state.get("chat_messages", [])) >= 10,
    },
    "resume_optimizer": {
        "name": "Resume Optimizer",
        "description": "Upload and analyze your resume",
        "emoji": "📄",
        "points": 15,
        "condition": lambda _: st.session_state.get("resume_uploaded", False),
    },
    "interview_master": {
        "name": "Interview Master",
        "description": "Complete 3 mock interviews",
        "emoji": "🎤",
        "points": 40,
        "condition": lambda _: st.session_state.get("interview_count", 0) >= 3,
    },
    "streak_champion": {
        "name": "Streak Champion",
        "description": "Maintain a 7-day login streak",
        "emoji": "🔥",
        "points": 100,
        "condition": lambda _: st.session_state.get("login_streak", 0) >= 7,
    },
    "skill_master": {
        "name": "Skill Master",
        "description": "Assess 5 different skills",
        "emoji": "⭐",
        "points": 75,
        "condition": lambda profile: profile and len(profile.get("skill_assessment", {}).get("technical_skills", {})) >= 5,
    },
    "project_hero": {
        "name": "Project Hero",
        "description": "Complete 5 project ideas",
        "emoji": "💻",
        "points": 60,
        "condition": lambda _: st.session_state.get("projects_completed", 0) >= 5,
    },
}


def initialize_gamification():
    """Initialize gamification in session state."""
    if "earned_badges" not in st.session_state:
        st.session_state.earned_badges = []
    
    if "total_xp" not in st.session_state:
        st.session_state.total_xp = 0
    
    if "login_streak" not in st.session_state:
        st.session_state.login_streak = 1
    
    if "last_login" not in st.session_state:
        st.session_state.last_login = datetime.now().isoformat()


def check_achievements(profile):
    """Check and award achievements."""
    initialize_gamification()
    
    earned = st.session_state.earned_badges
    
    for badge_id, achievement in ACHIEVEMENTS.items():
        if badge_id not in earned:
            try:
                if achievement["condition"](profile):
                    earned.append(badge_id)
                    st.session_state.total_xp += achievement["points"]
                    return badge_id, achievement
            except:
                pass
    
    return None, None


def update_login_streak():
    """Update login streak based on consecutive days."""
    last_login = datetime.fromisoformat(st.session_state.last_login)
    today = datetime.now()
    
    days_diff = (today.date() - last_login.date()).days
    
    if days_diff == 0:
        # Same day, no change
        pass
    elif days_diff == 1:
        # Consecutive day
        st.session_state.login_streak += 1
    else:
        # Streak broken
        st.session_state.login_streak = 1
    
    st.session_state.last_login = datetime.now().isoformat()


def render_achievements():
    """Render achievements and gamification interface."""
    lang = st.session_state.get("language", "en")
    
    st.markdown("""
    <div class="module-header">
        <div class="module-icon">🏆</div>
        <div>
            <h2>Achievements & Progress</h2>
            <p>Track your accomplishments and earn badges on your career journey</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize
    initialize_gamification()
    update_login_streak()
    
    # XP and Streak Display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total XP", st.session_state.total_xp, "Points")
    
    with col2:
        st.metric("Login Streak", st.session_state.login_streak, "Days 🔥")
    
    with col3:
        badges_earned = len(st.session_state.earned_badges)
        total_badges = len(ACHIEVEMENTS)
        st.metric("Badges Earned", f"{badges_earned}/{total_badges}", "")
    
    st.divider()
    
    # Check for new achievements
    if st.session_state.get("current_profile"):
        new_badge_id, new_achievement = check_achievements(st.session_state.current_profile)
        if new_badge_id and new_achievement:
            st.success(f"🎉 **New Achievement!** {new_achievement['emoji']} {new_achievement['name']}")
            st.subheader(f"{new_achievement['emoji']} {new_achievement['name']}")
            st.write(new_achievement['description'])
            st.info(f"**+{new_achievement['points']} XP**")
    
    st.divider()
    
    # Earned Badges
    st.subheader("🏅 Earned Badges")
    earned = st.session_state.earned_badges
    
    if earned:
        badges_per_row = 3
        for i in range(0, len(earned), badges_per_row):
            cols = st.columns(badges_per_row)
            for j, col in enumerate(cols):
                badge_idx = i + j
                if badge_idx < len(earned):
                    badge_id = earned[badge_idx]
                    badge_info = ACHIEVEMENTS[badge_id]
                    with col:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 1rem; background: #1f1f2e; border-radius: 10px; border: 2px solid #6C63FF;">
                            <div style="font-size: 3rem; margin-bottom: 0.5rem;">{badge_info['emoji']}</div>
                            <strong>{badge_info['name']}</strong>
                            <p style="font-size: 0.85rem; color: #999;">{badge_info['description']}</p>
                            <span style="background: #6C63FF; color: white; padding: 0.25rem 0.5rem; border-radius: 5px; font-size: 0.8rem;">+{badge_info['points']} XP</span>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.info("📌 No badges earned yet. Complete activities to earn badges!")
    
    st.divider()
    
    # Unearned Badges (Locked)
    st.subheader("🔒 Locked Badges")
    unearned = {k: v for k, v in ACHIEVEMENTS.items() if k not in earned}
    
    if unearned:
        badges_per_row = 3
        badge_list = list(unearned.items())
        for i in range(0, len(badge_list), badges_per_row):
            cols = st.columns(badges_per_row)
            for j, col in enumerate(cols):
                badge_idx = i + j
                if badge_idx < len(badge_list):
                    badge_id, badge_info = badge_list[badge_idx]
                    with col:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 1rem; background: #0f1020; border-radius: 10px; border: 2px solid #333; opacity: 0.6;">
                            <div style="font-size: 3rem; margin-bottom: 0.5rem; opacity: 0.4;">{badge_info['emoji']}</div>
                            <strong style="opacity: 0.7;">{badge_info['name']}</strong>
                            <p style="font-size: 0.85rem; color: #666;">{badge_info['description']}</p>
                            <span style="background: #444; color: #999; padding: 0.25rem 0.5rem; border-radius: 5px; font-size: 0.8rem;">+{badge_info['points']} XP</span>
                        </div>
                        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Level calculation
    level = st.session_state.total_xp // 100 + 1
    xp_for_next_level = ((level) * 100) - st.session_state.total_xp
    
    st.subheader(f"⭐ Level {level}")
    progress_pct = (st.session_state.total_xp % 100) / 100
    st.progress(progress_pct, text=f"{st.session_state.total_xp % 100}/100 XP to next level")
    st.caption(f"Next level in {xp_for_next_level} XP")
