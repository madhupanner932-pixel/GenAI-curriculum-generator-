"""
translations.py — Multi-language Support
English & Tamil translations for the Career Assistant Platform.
"""

TRANSLATIONS = {
    "en": {
        # Sidebar
        "sidebar_logo": "Career Assistant",
        "sidebar_subtitle": "AI-Powered Career Guidance Platform",
        "profile_management": "👤 Profile Management",
        "select_profile": "Select Profile",
        "no_profiles": "📌 No profiles yet. Create one below!",
        "profile_loaded": "✅ Loaded:",
        "create_new_profile": "➕ Create New Profile",
        "profile_name": "Profile Name",
        "career_field": "Career Field",
        "experience_level": "Experience Level",
        "career_goals": "Career Goals",
        "create_profile": "✨ Create Profile",
        "current_profile": "📋 Current Profile",
        "profile_name_label": "Name:",
        "profile_field_label": "Field:",
        "profile_level_label": "Level:",
        "delete_profile": "Delete profile",
        "configuration": "⚙️ Configuration",
        "api_status": "API Status",
        "api_configured": "✅ API key configured",
        "api_missing": "⚠️ API key missing",
        "quick_setup": "📖 Quick Setup Guide",
        
        # Navigation
        "nav_roadmap": "🗺️  Career Roadmap",
        "nav_chat": "💬  Smart Chat",
        "nav_projects": "💡  Project Ideas",
        "nav_resume": "📄  Resume Analyzer",
        "nav_interview": "🎤  Mock Interview",
        "nav_skills": "🎯  Skill Assessment",
        "nav_progress": "📊  Progress & Analytics",
        "nav_gap": "⚙️  Gap Analysis",
        "nav_gamification": "🏆  Achievements",
        "nav_mentor": "🤝  Mentor Matching",
        
        # Common messages
        "please_select_profile": "⚠️ Please select or create a career profile first!",
        "profile_created_success": "✅ Profile created successfully!",
        "profile_deleted_success": "✅ Profile deleted successfully!",
        "loading": "Loading...",
        
        # Language
        "language": "Language",
        "select_language": "Select Language",
        "english": "English",
        "tamil": "தமிழ்",
    },
    "ta": {
        # Sidebar
        "sidebar_logo": "சேர்ப்பு உதவியாளர்",
        "sidebar_subtitle": "AI-இயக்கப்பட்ட தொழில் வழிகாட்டல் தளம்",
        "profile_management": "👤 சுயவிவர நிர்வாகம்",
        "select_profile": "சுயவிவரத்தைத் தேர்ந்தெடுக்கவும்",
        "no_profiles": "📌 இன்னும் சுயவிவரங்கள் இல்லை. கீழே ஒன்றை உருவாக்கவும்!",
        "profile_loaded": "✅ ஏற்றப்பட்டது:",
        "create_new_profile": "➕ புதிய சுயவிவரத்தை உருவாக்கவும்",
        "profile_name": "சுயவிவர பெயர்",
        "career_field": "தொழில் துறை",
        "experience_level": "அভிজ்ञதை நிலை",
        "career_goals": "தொழில் இலக்குகள்",
        "create_profile": "✨ சுயவிவரத்தை உருவாக்கவும்",
        "current_profile": "📋 தற்போதைய சுயவிவரம்",
        "profile_name_label": "பெயர்:",
        "profile_field_label": "துறை:",
        "profile_level_label": "நிலை:",
        "delete_profile": "சுயவிவரத்தை நீக்கவும்",
        "configuration": "⚙️ உள்ளமைவு",
        "api_status": "API நிலை",
        "api_configured": "✅ API விசை உள்ளமைக்கப்பட்டுள்ளது",
        "api_missing": "⚠️ API விசை விடுபட்டுள்ளது",
        "quick_setup": "📖 விரைவு அமைப்பு வழிகாட்டி",
        
        # Navigation
        "nav_roadmap": "🗺️  தொழில் வழிபாணை",
        "nav_chat": "💬  ஸ்மார்ட் சாட்",
        "nav_projects": "💡  திட்ட विचार",
        "nav_resume": "📄  மறுசொல் பகுப்பாய்வுகாரன்",
        "nav_interview": "🎤  மாக் साक्षात्कार",
        "nav_skills": "🎯  திறன் மதிப்பீடு",
        "nav_progress": "📊  முன்னேற்றம் & பகுப்பாய்வு",
        "nav_gap": "⚙️  இடைவெளி பகுப்பாய்வு",
        "nav_gamification": "🏆  சாதனைகள்",
        "nav_mentor": "🤝  மெண்டர் பொருத்தம்",
        
        # Common messages
        "please_select_profile": "⚠️ முதலில் சுயவிவரத்தைத் தேர்ந்தெடுக்கவும் அல்லது உருவாக்கவும்!",
        "profile_created_success": "✅ சுயவிவரம் வெற்றிகரமாக உருவாக்கப்பட்டது!",
        "profile_deleted_success": "✅ சுயவிவரம் வெற்றிகரமாக நீக்கப்பட்டது!",
        "loading": "ஏற்றுதல்...",
        
        # Language
        "language": "மொழி",
        "select_language": "மொழியைத் தேர்ந்தெடுக்கவும்",
        "english": "English",
        "tamil": "தமிழ்",
    }
}


def get_text(key, language="en"):
    """Get translated text for a key."""
    lang_dict = TRANSLATIONS.get(language, TRANSLATIONS["en"])
    return lang_dict.get(key, key)


def get_all_translations(language="en"):
    """Get all translations for a language."""
    return TRANSLATIONS.get(language, TRANSLATIONS["en"])
