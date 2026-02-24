"""
profile_manager.py — User Profile Management
Handle profile creation, storage, and retrieval.
"""

import json
import os
from datetime import datetime
from pathlib import Path
import pandas as pd


class ProfileManager:
    """Manage user career profiles."""
    
    def __init__(self, profiles_dir="data/profiles"):
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
    
    def create_profile(self, profile_name, data):
        """Create a new profile."""
        profile_data = {
            "name": profile_name,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            **data
        }
        
        file_path = self.profiles_dir / f"{profile_name}.json"
        with open(file_path, 'w') as f:
            json.dump(profile_data, f, indent=2)
        
        return profile_data
    
    def load_profile(self, profile_name):
        """Load a profile by name."""
        file_path = self.profiles_dir / f"{profile_name}.json"
        
        if not file_path.exists():
            return None
        
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def update_profile(self, profile_name, data):
        """Update an existing profile."""
        profile = self.load_profile(profile_name)
        if not profile:
            return None
        
        profile.update(data)
        profile["updated_at"] = datetime.now().isoformat()
        
        file_path = self.profiles_dir / f"{profile_name}.json"
        with open(file_path, 'w') as f:
            json.dump(profile, f, indent=2)
        
        return profile
    
    def list_profiles(self):
        """List all profiles."""
        profiles = []
        for file_path in self.profiles_dir.glob("*.json"):
            with open(file_path, 'r') as f:
                profile = json.load(f)
                profiles.append(profile)
        
        return sorted(profiles, key=lambda x: x.get("updated_at", ""), reverse=True)
    
    def delete_profile(self, profile_name):
        """Delete a profile."""
        file_path = self.profiles_dir / f"{profile_name}.json"
        
        if file_path.exists():
            file_path.unlink()
            return True
        
        return False
    
    def export_profile(self, profile_name, export_format="json"):
        """Export a profile to different formats."""
        profile = self.load_profile(profile_name)
        if not profile:
            return None
        
        if export_format == "json":
            return json.dumps(profile, indent=2)
        
        elif export_format == "csv":
            # Convert to DataFrame for CSV export
            df = pd.json_normalize(profile)
            return df.to_csv(index=False)
        
        return None
    
    def import_profile(self, profile_name, data, format="json"):
        """Import a profile from different formats."""
        if format == "json":
            if isinstance(data, str):
                profile_data = json.loads(data)
            else:
                profile_data = data
        else:
            profile_data = data
        
        return self.create_profile(profile_name, profile_data)
    
    def get_profile_stats(self, profile_name):
        """Get statistics for a profile."""
        profile = self.load_profile(profile_name)
        if not profile:
            return None
        
        stats = {
            "name": profile.get("name", ""),
            "career_field": profile.get("career_field", ""),
            "experience_level": profile.get("experience_level", ""),
            "created_at": profile.get("created_at", ""),
            "updated_at": profile.get("updated_at", ""),
            "has_roadmap": "roadmap_data" in profile,
            "has_skills": "skill_assessment" in profile,
            "has_progress": "progress_data" in profile,
        }
        
        return stats
    
    def merge_profiles(self, source_name, target_name):
        """Merge source profile into target profile."""
        source = self.load_profile(source_name)
        target = self.load_profile(target_name)
        
        if not source or not target:
            return None
        
        # Merge data (target takes precedence on conflicts)
        merged = {**source, **target}
        merged["updated_at"] = datetime.now().isoformat()
        
        file_path = self.profiles_dir / f"{target_name}.json"
        with open(file_path, 'w') as f:
            json.dump(merged, f, indent=2)
        
        return merged


class ProgressTracker:
    """Track user progress across profiles."""
    
    def __init__(self, data_dir="data/progress"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def log_activity(self, profile_name, activity_type, details):
        """Log an activity for a profile."""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "type": activity_type,
            "details": details
        }
        
        log_file = self.data_dir / f"{profile_name}_log.json"
        
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_data)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def get_activity_log(self, profile_name):
        """Get activity log for a profile."""
        log_file = self.data_dir / f"{profile_name}_log.json"
        
        if not log_file.exists():
            return []
        
        with open(log_file, 'r') as f:
            return json.load(f)
    
    def get_statistics(self, profile_name):
        """Get statistics for profile progress."""
        logs = self.get_activity_log(profile_name)
        
        stats = {
            "total_activities": len(logs),
            "activity_types": {},
            "recent_activity": logs[-5:] if logs else [],
        }
        
        # Count activity types
        for log in logs:
            activity_type = log.get("type", "unknown")
            stats["activity_types"][activity_type] = stats["activity_types"].get(activity_type, 0) + 1
        
        return stats
