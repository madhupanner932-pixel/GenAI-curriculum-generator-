# ============================================================================
# DATA PERSISTENCE & STORAGE UTILITIES
# ============================================================================
# Stores user profiles, roadmaps, assessments, and career data locally

import json
import os
from datetime import datetime
from pathlib import Path

# Define storage directory
STORAGE_DIR = Path("data")
PROFILES_DIR = STORAGE_DIR / "profiles"
RESULTS_DIR = STORAGE_DIR / "results"

def ensure_storage_dirs():
    """Create storage directories if they don't exist"""
    STORAGE_DIR.mkdir(exist_ok=True)
    PROFILES_DIR.mkdir(exist_ok=True)
    RESULTS_DIR.mkdir(exist_ok=True)

ensure_storage_dirs()

# ============================================================================
# PROFILE MANAGEMENT
# ============================================================================

def save_profile(profile_name: str, profile_data: dict) -> bool:
    """Save a user profile"""
    try:
        profile_file = PROFILES_DIR / f"{profile_name}.json"
        profile_data["created_at"] = profile_data.get("created_at", datetime.now().isoformat())
        profile_data["updated_at"] = datetime.now().isoformat()
        
        with open(profile_file, "w") as f:
            json.dump(profile_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving profile: {e}")
        return False

def load_profile(profile_name: str) -> dict:
    """Load a user profile"""
    try:
        profile_file = PROFILES_DIR / f"{profile_name}.json"
        if profile_file.exists():
            with open(profile_file, "r") as f:
                return json.load(f)
        return None
    except Exception as e:
        print(f"Error loading profile: {e}")
        return None

def get_all_profiles() -> list:
    """Get list of all saved profiles"""
    try:
        profiles = []
        for file in PROFILES_DIR.glob("*.json"):
            profiles.append(file.stem)
        return sorted(profiles)
    except Exception as e:
        print(f"Error getting profiles: {e}")
        return []

def delete_profile(profile_name: str) -> bool:
    """Delete a user profile"""
    try:
        profile_file = PROFILES_DIR / f"{profile_name}.json"
        if profile_file.exists():
            profile_file.unlink()
            return True
        return False
    except Exception as e:
        print(f"Error deleting profile: {e}")
        return False

# ============================================================================
# RESULTS & ASSESSMENT STORAGE
# ============================================================================

def save_roadmap(profile_name: str, roadmap_data: str) -> bool:
    """Save generated roadmap"""
    try:
        ensure_storage_dirs()
        result_file = RESULTS_DIR / f"{profile_name}_roadmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        result = {
            "type": "roadmap",
            "profile": profile_name,
            "content": roadmap_data,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(result_file, "w") as f:
            json.dump(result, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving roadmap: {e}")
        return False

def save_resume_analysis(profile_name: str, analysis_data: str) -> bool:
    """Save resume analysis"""
    try:
        ensure_storage_dirs()
        result_file = RESULTS_DIR / f"{profile_name}_resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        result = {
            "type": "resume_analysis",
            "profile": profile_name,
            "content": analysis_data,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(result_file, "w") as f:
            json.dump(result, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving resume analysis: {e}")
        return False

def save_interview_session(profile_name: str, session_data: dict) -> bool:
    """Save mock interview session"""
    try:
        ensure_storage_dirs()
        result_file = RESULTS_DIR / f"{profile_name}_interview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        session_data["type"] = "interview"
        session_data["profile"] = profile_name
        session_data["timestamp"] = datetime.now().isoformat()
        
        with open(result_file, "w") as f:
            json.dump(session_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving interview session: {e}")
        return False

# ============================================================================
# ANALYTICS & STATISTICS
# ============================================================================

def get_profile_stats(profile_name: str) -> dict:
    """Get statistics for a profile"""
    try:
        profile = load_profile(profile_name)
        if not profile:
            return {}
        
        # Count results
        results = list(RESULTS_DIR.glob(f"{profile_name}_*.json"))
        
        roadmap_count = len(list(RESULTS_DIR.glob(f"{profile_name}_roadmap_*.json")))
        resume_count = len(list(RESULTS_DIR.glob(f"{profile_name}_resume_*.json")))
        interview_count = len(list(RESULTS_DIR.glob(f"{profile_name}_interview_*.json")))
        
        stats = {
            "profile_name": profile_name,
            "skill_level": profile.get("user_level", "Unknown"),
            "target_role": profile.get("target_role", "Unknown"),
            "roadmaps_generated": roadmap_count,
            "resumes_analyzed": resume_count,
            "interviews_completed": interview_count,
            "total_interactions": roadmap_count + resume_count + interview_count,
            "created_at": profile.get("created_at", "Unknown"),
            "updated_at": profile.get("updated_at", "Unknown")
        }
        
        return stats
    except Exception as e:
        print(f"Error getting profile stats: {e}")
        return {}

def get_all_stats() -> dict:
    """Get statistics for all profiles"""
    stats = {}
    for profile in get_all_profiles():
        stats[profile] = get_profile_stats(profile)
    return stats

# ============================================================================
# EXPORT & IMPORT
# ============================================================================

def export_profile_as_text(profile_name: str) -> str:
    """Export profile data as formatted text"""
    profile = load_profile(profile_name)
    if not profile:
        return "Profile not found"
    
    text = f"""
═══════════════════════════════════════════════════════════════
CAREER PROFILE
═══════════════════════════════════════════════════════════════

Profile Name: {profile_name}
Created: {profile.get('created_at', 'Unknown')}
Last Updated: {profile.get('updated_at', 'Unknown')}

PROFILE DETAILS
───────────────────────────────────────────────────────────────
Current Skill Level: {profile.get('user_level', 'Not set')}
Target Role/Field: {profile.get('target_role', 'Not set')}
Daily Time Availability: {profile.get('daily_availability', 'Not set')}
Target Timeline: {profile.get('timeline', 'Not set')}

STATISTICS
───────────────────────────────────────────────────────────────
"""
    
    stats = get_profile_stats(profile_name)
    text += f"""Roadmaps Generated: {stats.get('roadmaps_generated', 0)}
Resume Analyses: {stats.get('resumes_analyzed', 0)}
Interview Sessions: {stats.get('interviews_completed', 0)}
Total Interactions: {stats.get('total_interactions', 0)}

═══════════════════════════════════════════════════════════════
"""
    return text

def backup_all_data() -> bool:
    """Backup all user data"""
    try:
        from shutil import copytree
        from datetime import datetime
        
        backup_dir = Path("backups") / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if STORAGE_DIR.exists():
            copytree(STORAGE_DIR, backup_dir)
            return True
        return False
    except Exception as e:
        print(f"Error backing up data: {e}")
        return False

def restore_from_backup(backup_path: str) -> bool:
    """Restore data from backup"""
    try:
        from shutil import copytree
        
        backup_path = Path(backup_path)
        if backup_path.exists():
            # Remove old data
            import shutil
            if STORAGE_DIR.exists():
                shutil.rmtree(STORAGE_DIR)
            # Restore backup
            copytree(backup_path, STORAGE_DIR)
            return True
        return False
    except Exception as e:
        print(f"Error restoring backup: {e}")
        return False
