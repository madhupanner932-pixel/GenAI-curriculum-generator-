# 👤 Profile Management System

## Overview

The Career Assistant Platform now includes a comprehensive profile management system that enables users to create, manage, and track multiple career profiles with persistent data storage.

## Features

### 1. **Profile Creation**
Users can create new career profiles with the following information:
- **Profile Name**: Unique identifier (e.g., "John Doe", "ML Engineer Path")
- **Career Field**: Selected from 10+ predefined fields:
  - Software Engineering
  - Data Science
  - Product Management
  - UX/UI Design
  - DevOps
  - Cloud Architecture
  - Machine Learning
  - Full Stack Web Dev
  - Mobile Development
  - Other
- **Experience Level**: Beginner → Intermediate → Advanced → Expert
- **Career Goals**: Free-text area for user's goals and aspirations

### 2. **Profile Selection & Switching**
- **Dropdown selector**: Quickly switch between saved profiles
- **Profile status display**: Shows current profile name, field, and level
- **Delete functionality**: Remove profiles with a single-click button

### 3. **Data Persistence**
All profile data is saved to JSON files in `data/profiles/` directory with automatic timestamps:
- Profile creation date
- Last update timestamp
- All nested data (assessments, progress, roadmaps)

### 4. **Integration with Modules**

#### ✅ Skill Assessment Module
- Pre-fill form with profile's career field
- Save skill assessments to profile
- Track technical and soft skills (1-10 scale)
- AI-powered improvement recommendations

#### ✅ Progress & Analytics Module
- Log career milestones, projects, and skill improvements
- Track in-progress learning activities
- Visualize progress with charts and metrics
- Automatic saving to profile

#### ✅ Career Roadmap Generator
- Pre-fill roadmap form with profile's career field and experience level
- Save generated roadmaps to profile with metadata
- Access previously saved roadmaps

#### ✅ Other Modules
- Chat, Projects, Resume Analyzer, and Mock Interview can reference profile data
- Profile context available in `st.session_state.current_profile`

## Architecture

### Session State Variables
```python
st.session_state.current_profile       # Current loaded profile (dict or None)
st.session_state.profile_manager       # ProfileManager instance
```

### Profile Data Structure
```json
{
  "name": "John Doe",
  "career_field": "Software Engineering",
  "experience_level": "Intermediate",
  "goals": "Become a senior full-stack developer...",
  "created_at": "2025-02-24T22:30:00",
  "updated_at": "2025-02-24T22:35:00",
  "skill_assessment": { ... },
  "progress_data": { ... },
  "roadmap_data": { ... }
}
```

### ProfileManager Class
Located in `utils/profile_manager.py`:

#### Methods
- `create_profile(name, data)` - Create new profile
- `load_profile(name)` - Load profile by name
- `update_profile(name, data)` - Update existing profile
- `list_profiles()` - Get all profiles
- `delete_profile(name)` - Delete profile
- `export_profile(name, format)` - Export to JSON/CSV
- `get_profile_stats(name)` - Get profile statistics

## Usage Guide

### Creating Your First Profile

1. Open the Career Assistant app
2. Look at the left sidebar under "👤 Profile Management"
3. Click "➕ Create New Profile"
4. Fill in:
   - Your name (or profile identifier)
   - Career field you're interested in
   - Your current experience level
   - Your career goals
5. Click "✨ Create Profile"

### Using Profile-Dependent Features

Once a profile is created:

1. **Skill Assessment**
   - Navigate to "🎯 Skill Assessment" tab
   - Rate your proficiency in various skills
   - Get AI-powered recommendations
   - Results are automatically saved to profile

2. **Progress Tracking**
   - Navigate to "📊 Progress & Analytics" tab
   - Use the expander to log activities:
     - Completed milestones
     - Started learning new skills
     - Finished projects
     - Improved existing skills
   - View progression in Overview, Milestones, and Analytics tabs

3. **Career Roadmap**
   - Navigate to "🗺️ Career Roadmap" tab
   - Pre-filled with your career field and experience level
   - Generate your roadmap
   - Save it to your profile for future reference

## Data Files

### Profile Storage
```
data/profiles/
├── John_Doe.json
├── Sarah_Smith.json
└── Alex_Johnson.json
```

### Progress Tracking
```
data/progress/
└── (Activity logs and detailed progress data)
```

## Features Enabled by Profiles

| Feature | Without Profile | With Profile |
|---------|-----------------|--------------|
| Career Roadmap | ✅ Works | ✅ Pre-filled, saveable |
| Skill Assessment | ❌ Warning shown | ✅ Full functionality |
| Progress Tracking | ❌ Warning shown | ✅ Full functionality |
| Chat, Projects, Resume | ✅ Works | ✅ Profile-aware |
| Interview Practice | ✅ Works | ✅ Profile-aware |

## Technical Integration

### Sidebar Profile Management (app.py)
```python
# Profile selection
pm = st.session_state.profile_manager
profiles = pm.list_profiles()
profile_names = [p["name"] for p in profiles]

# Create profile with form
# Update session state
st.session_state.current_profile = new_profile
```

### Modules Integration (skills.py, progress.py, roadmap.py)
```python
# Check for profile
if not st.session_state.current_profile:
    st.warning("Please select or create a profile first!")
    return

# Get profile data
profile = st.session_state.current_profile
career_field = profile.get("career_field")

# Save updates
profile["skill_assessment"] = assessment_data
st.session_state.profile_manager.update_profile(profile["name"], assessment_data)
```

## Error Handling

- **No profiles exist**: "📌 No profiles yet. Create one below!" message
- **Missing profile for dependent features**: "⚠️ Please select or create a career profile first!"
- **Duplicate profile names**: Will overwrite (consider adding uniqueness check in future)

## Future Enhancements

- [ ] Profile image/avatar support
- [ ] Profile sharing and collaboration
- [ ] Cloud sync for profiles
- [ ] Profile templates for common career paths
- [ ] Bulk profile import/export
- [ ] Profile analytics and insights

## Troubleshooting

### Profile not saving
- Check that `data/profiles/` directory exists
- Ensure write permissions in the directory
- Check browser console for errors

### Profile not loading after switching
- Refresh the page (Ctrl+R)
- Click the profile dropdown again
- Check that profile file exists in `data/profiles/`

### Session state reset
- **Note**: Streamlit resets session state on page reload
- Profile data is persisted in `data/profiles/` JSON files
- Reload profile from dropdown to restore in session

## Code Changes Summary

### Modified Files
- `app.py` - Added profile management UI in sidebar
- `modules/skills.py` - Integrated profile saving
- `modules/progress.py` - Integrated profile saving
- `modules/roadmap.py` - Integrated profile usage and saving

### New Session State Variables
- `st.session_state.current_profile` - Current active profile
- `st.session_state.profile_manager` - ProfileManager instance

### Profile Manager (utils/profile_manager.py)
- Already existed; fully utilized for this feature
- No modifications needed

