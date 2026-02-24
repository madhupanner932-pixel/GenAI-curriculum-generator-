# ============================================================================
# REPORT GENERATION UTILITIES
# ============================================================================
# Generates PDF reports, summaries, and exports

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import json

def generate_text_report(profile_name: str, stats: Dict, assessments: List[Dict] = None) -> str:
    """
    Generate a formatted text report
    
    Args:
        profile_name: Name of the profile
        stats: Profile statistics
        assessments: Optional list of assessment results
    
    Returns:
        Formatted report as string
    """
    report = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                      CAREER ASSISTANT - PROFILE REPORT                    ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 PROFILE INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Profile Name:          {profile_name}
Skill Level:           {stats.get('user_level', 'N/A')}
Target Role:           {stats.get('target_role', 'N/A')}
Daily Availability:    {stats.get('daily_availability', 'N/A')}
Target Timeline:       {stats.get('timeline', 'N/A')}
Created Date:          {stats.get('created_at', 'N/A')}
Last Updated:          {stats.get('updated_at', 'N/A')}

📊 ACTIVITY METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Roadmaps Generated:    {stats.get('roadmaps_generated', 0)}
Resumes Analyzed:      {stats.get('resumes_analyzed', 0)}
Interviews Completed:  {stats.get('interviews_completed', 0)}
--────────────────────────────────────────
Total Interactions:    {stats.get('total_interactions', 0)}

📈 PERFORMANCE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Engagement Level:      {get_engagement_level(stats)}
Progress Status:       {get_progress_status(stats)}
Recommended Focus:     {get_recommended_focus(stats)}

"""
    
    if assessments and len(assessments) > 0:
        report += """
🎯 ASSESSMENT RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        for assessment in assessments:
            topic = assessment.get('topic', 'Unknown')
            score = assessment.get('score', 0)
            level = assessment.get('level', 'N/A')
            report += f"\n✓ {topic:<30} {score:>5.1f}%  ({level})"
        report += "\n"
    
    report += f"""
{('═' * 80)}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Platform: Career Assistant Platform v2.0
{('═' * 80)}

NOTES:
- All statistics are automatically generated from your profile activity
- Use this report for resume/portfolio documentation
- Print or share this report to track your progress over time
- Assessments can be retaken to improve your score
"""
    
    return report

def generate_csv_export(profiles: List[Dict]) -> str:
    """
    Generate CSV export of multiple profiles
    
    Args:
        profiles: List of profile dictionaries
    
    Returns:
        CSV formatted string
    """
    if not profiles:
        return "No profiles to export"
    
    # CSV header
    headers = [
        "Profile Name",
        "Skill Level",
        "Target Role",
        "Daily Availability",
        "Timeline",
        "Roadmaps Generated",
        "Resumes Analyzed",
        "Interviews Completed",
        "Total Interactions",
        "Engagement Level",
        "Created Date",
        "Last Updated"
    ]
    
    csv = ",".join(headers) + "\n"
    
    # Data rows
    for profile in profiles:
        engagement = int(calculate_profile_engagement(profile) * 100) / 100
        row = [
            profile.get("profile_name", ""),
            profile.get("user_level", ""),
            profile.get("target_role", ""),
            profile.get("daily_availability", ""),
            profile.get("timeline", ""),
            str(profile.get("roadmaps_generated", 0)),
            str(profile.get("resumes_analyzed", 0)),
            str(profile.get("interviews_completed", 0)),
            str(profile.get("total_interactions", 0)),
            f"{engagement:.1f}",
            profile.get("created_at", "").split("T")[0],
            profile.get("updated_at", "").split("T")[0]
        ]
        # Escape quotes in values
        csv += ",".join(f'"{str(item).replace('"', '""')}"' for item in row) + "\n"
    
    return csv

def generate_json_export(profiles: List[Dict]) -> str:
    """
    Generate JSON export of profiles
    
    Args:
        profiles: List of profile dictionaries
    
    Returns:
        JSON formatted string
    """
    export_data = {
        "export_date": datetime.now().isoformat(),
        "total_profiles": len(profiles),
        "profiles": profiles
    }
    
    return json.dumps(export_data, indent=2)

def generate_summary_stats(profiles: List[Dict]) -> Dict:
    """
    Generate summary statistics across all profiles
    
    Args:
        profiles: List of profile dictionaries
    
    Returns:
        Dictionary with summary stats
    """
    if not profiles:
        return {
            "total_profiles": 0,
            "total_interactions": 0,
            "avg_interactions": 0,
            "total_roadmaps": 0,
            "total_resumes": 0,
            "total_interviews": 0,
            "avg_engagement": 0
        }
    
    total_interactions = sum(p.get("total_interactions", 0) for p in profiles)
    total_roadmaps = sum(p.get("roadmaps_generated", 0) for p in profiles)
    total_resumes = sum(p.get("resumes_analyzed", 0) for p in profiles)
    total_interviews = sum(p.get("interviews_completed", 0) for p in profiles)
    
    num_profiles = len(profiles)
    engagements = [calculate_profile_engagement(p) for p in profiles]
    avg_engagement = sum(engagements) / num_profiles if engagements else 0
    
    return {
        "total_profiles": num_profiles,
        "total_interactions": total_interactions,
        "avg_interactions": round(total_interactions / num_profiles, 2),
        "total_roadmaps": total_roadmaps,
        "total_resumes": total_resumes,
        "total_interviews": total_interviews,
        "avg_engagement": round(avg_engagement, 2),
        "export_date": datetime.now().isoformat()
    }

# ============================================================================
# ENGAGEMENT & STATUS HELPERS
# ============================================================================

def calculate_profile_engagement(stats: Dict) -> float:
    """
    Calculate engagement score for a profile (0-100)
    
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
    
    # Weighted calculation
    score = (interactions * 0.4) + (roadmaps * 10) + (resumes * 15) + (interviews * 20)
    
    return min(100.0, score)

def get_engagement_level(stats: Dict) -> str:
    """Get engagement level description"""
    engagement = calculate_profile_engagement(stats)
    
    if engagement >= 80:
        return "🟢 Highly Engaged"
    elif engagement >= 60:
        return "🟡 Moderately Engaged"
    elif engagement >= 40:
        return "🟠 Lightly Engaged"
    else:
        return "🔴 Minimal Engagement"

def get_progress_status(stats: Dict) -> str:
    """Get progress status description"""
    roadmaps = stats.get("roadmaps_generated", 0)
    resumes = stats.get("resumes_analyzed", 0)
    interviews = stats.get("interviews_completed", 0)
    
    completed = sum(1 for x in [roadmaps, resumes, interviews] if x > 0)
    
    if completed == 0:
        return "No Progress Yet"
    elif completed == 1:
        return "1/3 Modules Started"
    elif completed == 2:
        return "2/3 Modules Completed"
    else:
        return "All Modules Explored"

def get_recommended_focus(stats: Dict) -> str:
    """Get recommended focus area"""
    roadmaps = stats.get("roadmaps_generated", 0)
    resumes = stats.get("resumes_analyzed", 0)
    interviews = stats.get("interviews_completed", 0)
    
    if roadmaps == 0:
        return "Create a learning roadmap"
    elif resumes == 0:
        return "Upload and analyze your resume"
    elif interviews == 0:
        return "Practice mock interviews"
    elif interviews < 3:
        return "More interview practice"
    else:
        return "Take assessments or refine skills"

# ============================================================================
# MILESTONE & ACHIEVEMENT HELPERS
# ============================================================================

def get_milestones_achieved(stats: Dict) -> List[str]:
    """Get list of milestones achieved"""
    milestones = []
    
    if stats.get("roadmaps_generated", 0) > 0:
        milestones.append("✓ Created learning roadmap")
    
    if stats.get("roadmaps_generated", 0) >= 3:
        milestones.append("✓ Multiple roadmap iterations")
    
    if stats.get("resumes_analyzed", 0) > 0:
        milestones.append("✓ Analyzed resume")
    
    if stats.get("interviews_completed", 0) > 0:
        milestones.append("✓ Completed first interview")
    
    if stats.get("interviews_completed", 0) >= 5:
        milestones.append("✓ Interview practice veteran")
    
    if stats.get("total_interactions", 0) >= 50:
        milestones.append("✓ 50+ total interactions")
    
    if stats.get("total_interactions", 0) >= 100:
        milestones.append("✓ 100+ total interactions")
    
    return milestones

def generate_achievement_text(stats: Dict) -> str:
    """Generate achievement summary text"""
    milestones = get_milestones_achieved(stats)
    
    if not milestones:
        return "🎯 Start your journey by creating your first roadmap!"
    
    text = "🏆 ACHIEVEMENTS\n" + "━" * 40 + "\n"
    
    for milestone in milestones:
        text += f"{milestone}\n"
    
    return text
