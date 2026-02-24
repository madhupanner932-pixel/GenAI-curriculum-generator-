# ============================================================================
# VISUALIZATION UTILITIES
# ============================================================================
# Provides charts, graphs, and analytics visualizations

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

def format_stats_for_display(stats: Dict) -> Dict:
    """
    Format stats data for Streamlit display
    
    Args:
        stats: Statistics dictionary from storage.py
    
    Returns:
        Formatted stats with display-ready data
    """
    if not stats:
        return {
            "total_profiles": 0,
            "total_interactions": 0,
            "avg_roadmaps": 0,
            "avg_resumes": 0,
            "avg_interviews": 0
        }
    
    profiles = stats.get("all_profiles", [])
    total_profiles = len(profiles)
    
    if total_profiles == 0:
        return {
            "total_profiles": 0,
            "total_interactions": 0,
            "avg_roadmaps": 0,
            "avg_resumes": 0,
            "avg_interviews": 0
        }
    
    total_roadmaps = sum(p.get("roadmaps_generated", 0) for p in profiles)
    total_resumes = sum(p.get("resumes_analyzed", 0) for p in profiles)
    total_interviews = sum(p.get("interviews_completed", 0) for p in profiles)
    total_interactions = sum(p.get("total_interactions", 0) for p in profiles)
    
    return {
        "total_profiles": total_profiles,
        "total_interactions": total_interactions,
        "avg_roadmaps": round(total_roadmaps / total_profiles, 2),
        "avg_resumes": round(total_resumes / total_profiles, 2),
        "avg_interviews": round(total_interviews / total_profiles, 2),
        "roadmaps_total": total_roadmaps,
        "resumes_total": total_resumes,
        "interviews_total": total_interviews
    }

def create_metric_cards(stats: Dict) -> List[Dict]:
    """
    Create metric cards for dashboard
    
    Args:
        stats: Formatted statistics
    
    Returns:
        List of metric card dictionaries
    """
    return [
        {
            "label": "👥 Total Users",
            "value": stats.get("total_profiles", 0),
            "delta": "+new",
            "color": "blue"
        },
        {
            "label": "🛣️ Roadmaps Generated",
            "value": stats.get("roadmaps_total", 0),
            "delta": f"Avg: {stats.get('avg_roadmaps', 0)}",
            "color": "green"
        },
        {
            "label": "📄 Resumes Analyzed",
            "value": stats.get("resumes_total", 0),
            "delta": f"Avg: {stats.get('avg_resumes', 0)}",
            "color": "orange"
        },
        {
            "label": "🎙️ Interviews Completed",
            "value": stats.get("interviews_total", 0),
            "delta": f"Avg: {stats.get('avg_interviews', 0)}",
            "color": "purple"
        },
        {
            "label": "⚡ Total Interactions",
            "value": stats.get("total_interactions", 0),
            "delta": "system-wide",
            "color": "red"
        }
    ]

def get_module_usage_data(stats: List[Dict]) -> Dict:
    """
    Create module usage breakdown
    
    Args:
        stats: List of profile stats
    
    Returns:
        Dictionary with module counts for visualization
    """
    if not stats:
        return {
            "Roadmap": 0,
            "Chat": 0,
            "Projects": 0,
            "Resume": 0,
            "Interview": 0
        }
    
    # Estimate module usage from interaction counts
    total = sum(s.get("total_interactions", 1) for s in stats) or 1
    
    return {
        "Roadmap": max(1, int((total * 0.2))),
        "Chat": max(1, int((total * 0.3))),
        "Projects": max(1, int((total * 0.15))),
        "Resume": max(1, int((total * 0.2))),
        "Interview": max(1, int((total * 0.15)))
    }

def get_skill_distribution(assessments: List[Dict]) -> Dict:
    """
    Create skill level distribution
    
    Args:
        assessments: List of assessment results
    
    Returns:
        Dictionary with skill distribution
    """
    levels = {
        "Beginner": 0,
        "Intermediate": 0,
        "Proficient": 0,
        "Advanced": 0,
        "Expert": 0
    }
    
    if not assessments:
        return levels
    
    for assessment in assessments:
        level = assessment.get("level", "Beginner")
        if level in levels:
            levels[level] += 1
    
    return levels

def generate_progress_summary(profile_stats: Dict) -> str:
    """
    Generate human-readable progress summary
    
    Args:
        profile_stats: Profile statistics
    
    Returns:
        Formatted summary text
    """
    roadmaps = profile_stats.get("roadmaps_generated", 0)
    resumes = profile_stats.get("resumes_analyzed", 0)
    interviews = profile_stats.get("interviews_completed", 0)
    interactions = profile_stats.get("total_interactions", 0)
    
    summary = f"""
    📊 **Progress Summary**
    
    • Roadmaps Created: **{roadmaps}**
    • Resumes Analyzed: **{resumes}**
    • Interviews Completed: **{interviews}**
    • Total Interactions: **{interactions}**
    
    **Activity Status:**
    """
    
    if interactions == 0:
        summary += "\n🟡 No activity yet - Start by creating a learning roadmap!"
    elif interactions < 5:
        summary += "\n🟡 Just getting started - Keep building momentum!"
    elif interactions < 15:
        summary += "\n🟢 Good progress - You're on track!"
    else:
        summary += "\n✨ Excellent engagement - Keep up the great work!"
    
    return summary

def create_recommendation_summary(assessment_result: Dict) -> str:
    """
    Create recommendation based on assessment
    
    Args:
        assessment_result: Result from calculate_score
    
    Returns:
        Recommendation text
    """
    percentage = assessment_result.get("percentage", 0)
    level = assessment_result.get("level", "Beginner")
    
    recommendations = {
        "Expert": "🎓 Excellent! Consider sharing your knowledge or taking advanced projects.",
        "Advanced": "⭐ Great work! Focus on practical application and real-world projects.",
        "Proficient": "✓ Good foundation! Practice more to strengthen weak areas.",
        "Intermediate": "📚 You're making progress! Dedicate more time to concept mastery.",
        "Beginner": "💪 Keep learning! Focus on fundamentals and practice consistently."
    }
    
    return recommendations.get(level, "Continue your learning journey!")

def get_timeline_data(profiles: List[Dict]) -> Dict:
    """
    Create timeline data from profiles
    
    Args:
        profiles: List of profile data
    
    Returns:
        Timeline data for visualization
    """
    timeline = {}
    
    for profile in profiles:
        created_at = profile.get("created_at", "")
        if created_at:
            # Extract date (assuming ISO format YYYY-MM-DD)
            date = created_at.split("T")[0] if "T" in created_at else created_at
            timeline[date] = timeline.get(date, 0) + 1
    
    return timeline

# ============================================================================
# EXPORT FORMATTING
# ============================================================================

def format_profile_report(profile_name: str, stats: Dict, assessments: List[Dict] = None) -> str:
    """
    Format profile data as readable report
    
    Args:
        profile_name: Name of profile
        stats: Profile statistics
        assessments: Optional assessment results
    
    Returns:
        Formatted report text
    """
    report = f"""
╔══════════════════════════════════════════════════════════════════╗
║            CAREER ASSISTANT - PROFILE REPORT                    ║
╚══════════════════════════════════════════════════════════════════╝

📋 PROFILE INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Profile Name:          {profile_name}
Skill Level:           {stats.get('skill_level', 'N/A')}
Target Role:           {stats.get('target_role', 'N/A')}
Created:               {stats.get('created_at', 'N/A')}
Last Updated:          {stats.get('updated_at', 'N/A')}

📊 ACTIVITY METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Roadmaps Generated:    {stats.get('roadmaps_generated', 0)}
Resumes Analyzed:      {stats.get('resumes_analyzed', 0)}
Interviews Completed:  {stats.get('interviews_completed', 0)}
Total Interactions:    {stats.get('total_interactions', 0)}

"""
    
    if assessments:
        report += """
🎯 ASSESSMENT RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        for assessment in assessments:
            report += f"\n• {assessment.get('topic', 'N/A')}: {assessment.get('percentage', 0)}% ({assessment.get('level', 'N/A')})"
    
    report += "\n\n" + "═" * 64 + "\n"
    report += "Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
    
    return report

def create_csv_export(profiles: List[Dict]) -> str:
    """
    Create CSV export of profiles
    
    Args:
        profiles: List of profile data
    
    Returns:
        CSV formatted string
    """
    if not profiles:
        return "No data to export"
    
    headers = ["Profile Name", "Skill Level", "Target Role", "Roadmaps", "Resumes", "Interviews", "Total Interactions", "Created"]
    csv = ",".join(headers) + "\n"
    
    for profile in profiles:
        row = [
            profile.get("profile_name", ""),
            profile.get("skill_level", ""),
            profile.get("target_role", ""),
            str(profile.get("roadmaps_generated", 0)),
            str(profile.get("resumes_analyzed", 0)),
            str(profile.get("interviews_completed", 0)),
            str(profile.get("total_interactions", 0)),
            profile.get("created_at", "")
        ]
        csv += ",".join(f'"{item}"' for item in row) + "\n"
    
    return csv

# ============================================================================
# PERFORMANCE METRICS
# ============================================================================

def calculate_engagement_score(stats: Dict) -> float:
    """
    Calculate engagement score 0-100
    
    Args:
        stats: Profile statistics
    
    Returns:
        Engagement score
    """
    if not stats:
        return 0.0
    
    interactions = stats.get("total_interactions", 0)
    roadmaps = stats.get("roadmaps_generated", 0)
    resumes = stats.get("resumes_analyzed", 0)
    interviews = stats.get("interviews_completed", 0)
    
    # Weighted scoring
    score = (interactions * 0.4) + (roadmaps * 10) + (resumes * 15) + (interviews * 20)
    
    # Cap at 100
    return min(100.0, score)

def get_next_recommended_action(stats: Dict) -> str:
    """
    Recommend next action based on profile stats
    
    Args:
        stats: Profile statistics
    
    Returns:
        Recommendation text
    """
    roadmaps = stats.get("roadmaps_generated", 0)
    resumes = stats.get("resumes_analyzed", 0)
    interviews = stats.get("interviews_completed", 0)
    
    if roadmaps == 0:
        return "🛣️ Start by creating a learning roadmap to guide your journey"
    elif resumes == 0 and roadmaps > 0:
        return "📄 Upload your resume for analysis and improvement suggestions"
    elif interviews == 0 and resumes > 0:
        return "🎙️ Practice with mock interviews to prepare for real conversations"
    elif roadmaps > 0 and resumes > 0 and interviews > 0:
        return "✨ You've covered all modules! Take assessments to validate your skills"
    else:
        return "💬 Continue with chat discussions to deepen your knowledge"
