"""
export_import.py — Profile Export & Import Utilities
Handle data export and import in multiple formats.
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from io import StringIO, BytesIO
import zipfile


class ProfileExporter:
    """Export profiles to various formats."""
    
    @staticmethod
    def to_json(profile):
        """Export profile as JSON string."""
        return json.dumps(profile, indent=2)
    
    @staticmethod
    def to_csv(profile):
        """Export profile as CSV string."""
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=profile.keys())
        writer.writeheader()
        writer.writerow(profile)
        return output.getvalue()
    
    @staticmethod
    def to_markdown(profile):
        """Export profile as Markdown."""
        md = f"""# {profile.get('name', 'Career Profile')}

## Career Information
- **Field**: {profile.get('career_field', 'N/A')}
- **Experience Level**: {profile.get('experience_level', 'N/A')}
- **Created**: {profile.get('created_at', 'N/A')}
- **Updated**: {profile.get('updated_at', 'N/A')}

## Profile Data
"""
        
        for key, value in profile.items():
            if key not in ['name', 'career_field', 'experience_level', 'created_at', 'updated_at']:
                if isinstance(value, (dict, list)):
                    md += f"\n### {key.replace('_', ' ').title()}\n"
                    md += f"```json\n{json.dumps(value, indent=2)}\n```\n"
                else:
                    md += f"- **{key.replace('_', ' ').title()}**: {value}\n"
        
        return md
    
    @staticmethod
    def to_html(profile):
        """Export profile as HTML."""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{profile.get('name', 'Career Profile')}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #6C63FF;
            border-bottom: 2px solid #6C63FF;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #333;
            margin-top: 20px;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin: 15px 0;
        }}
        .info-item {{
            background: #f9f9f9;
            padding: 10px;
            border-left: 4px solid #6C63FF;
        }}
        .label {{
            font-weight: bold;
            color: #6C63FF;
        }}
        pre {{
            background: #f0f0f0;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{profile.get('name', 'Career Profile')}</h1>
        
        <h2>Career Information</h2>
        <div class="info-grid">
            <div class="info-item">
                <span class="label">Field:</span><br>
                {profile.get('career_field', 'N/A')}
            </div>
            <div class="info-item">
                <span class="label">Experience:</span><br>
                {profile.get('experience_level', 'N/A')}
            </div>
            <div class="info-item">
                <span class="label">Created:</span><br>
                {profile.get('created_at', 'N/A')}
            </div>
            <div class="info-item">
                <span class="label">Updated:</span><br>
                {profile.get('updated_at', 'N/A')}
            </div>
        </div>
        
        <h2>Full Profile Data</h2>
        <pre>{json.dumps(profile, indent=2)}</pre>
    </div>
</body>
</html>
"""
        return html


class ProfileImporter:
    """Import profiles from various formats."""
    
    @staticmethod
    def from_json(json_string):
        """Import profile from JSON string."""
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {str(e)}")
    
    @staticmethod
    def from_csv(csv_string):
        """Import profile from CSV string."""
        try:
            reader = csv.DictReader(StringIO(csv_string))
            data = next(reader)
            return dict(data) if data else {}
        except Exception as e:
            raise ValueError(f"Invalid CSV: {str(e)}")
    
    @staticmethod
    def from_dict(data_dict):
        """Import profile from dictionary."""
        if not isinstance(data_dict, dict):
            raise ValueError("Input must be a dictionary")
        return data_dict


class BulkExportManager:
    """Manage bulk export of multiple profiles."""
    
    @staticmethod
    def export_all_profiles_zip(profiles_list):
        """Export all profiles as a ZIP file."""
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for profile in profiles_list:
                profile_name = profile.get('name', 'profile')
                
                # Add JSON file
                json_content = ProfileExporter.to_json(profile)
                zip_file.writestr(f"{profile_name}.json", json_content)
                
                # Add Markdown file
                md_content = ProfileExporter.to_markdown(profile)
                zip_file.writestr(f"{profile_name}.md", md_content)
                
                # Add HTML file
                html_content = ProfileExporter.to_html(profile)
                zip_file.writestr(f"{profile_name}.html", html_content)
        
        zip_buffer.seek(0)
        return zip_buffer
    
    @staticmethod
    def create_backup_zip(profiles_list, progress_logs):
        """Create a complete backup ZIP with all data."""
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            # Add profiles
            profiles_dir = "profiles/"
            for profile in profiles_list:
                profile_name = profile.get('name', 'profile')
                json_content = ProfileExporter.to_json(profile)
                zip_file.writestr(f"{profiles_dir}{profile_name}.json", json_content)
            
            # Add progress logs
            logs_dir = "progress_logs/"
            for log_name, log_data in progress_logs.items():
                json_content = json.dumps(log_data, indent=2)
                zip_file.writestr(f"{logs_dir}{log_name}.json", json_content)
            
            # Add metadata
            metadata = {
                "backup_date": datetime.now().isoformat(),
                "total_profiles": len(profiles_list),
                "total_progress_logs": len(progress_logs),
                "version": "1.0"
            }
            zip_file.writestr("BACKUP_METADATA.json", json.dumps(metadata, indent=2))
        
        zip_buffer.seek(0)
        return zip_buffer


class DataMigration:
    """Handle data migration and recovery."""
    
    @staticmethod
    def validate_profile(profile):
        """Validate profile data structure."""
        required_fields = ['name', 'career_field', 'experience_level']
        
        for field in required_fields:
            if field not in profile or not profile[field]:
                raise ValueError(f"Missing required field: {field}")
        
        return True
    
    @staticmethod
    def merge_profile_updates(old_profile, new_data):
        """Safely merge updates into existing profile."""
        merged = old_profile.copy()
        
        # Only update specific fields, preserve history
        mergeable_fields = [
            'career_field', 'experience_level', 'goal', 'interests',
            'roadmap_data', 'skill_assessment', 'progress_data'
        ]
        
        for field in mergeable_fields:
            if field in new_data:
                merged[field] = new_data[field]
        
        merged['updated_at'] = datetime.now().isoformat()
        return merged
    
    @staticmethod
    def recover_from_backup(backup_zip_path):
        """Recover profiles from backup ZIP."""
        recovered_profiles = []
        
        try:
            with zipfile.ZipFile(backup_zip_path, 'r') as zip_file:
                for file_name in zip_file.namelist():
                    if file_name.endswith('.json') and 'profiles/' in file_name:
                        json_data = zip_file.read(file_name).decode('utf-8')
                        profile = json.loads(json_data)
                        recovered_profiles.append(profile)
            
            return recovered_profiles
        except Exception as e:
            raise ValueError(f"Error recovering from backup: {str(e)}")
