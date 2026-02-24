"""
dashboard.py — Flask Web Dashboard
Web interface for Career Assistant Platform
Run with: python dashboard.py
"""

from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
import json
from pathlib import Path
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.profile_manager import ProfileManager, ProgressTracker

# Initialize Flask app
app = Flask(__name__, static_url_path='/static', static_folder='dashboard/static')
CORS(app)

# Initialize managers
profile_mgr = ProfileManager()
progress_tracker = ProgressTracker()


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Serve main dashboard page."""
    return render_template('index.html')


@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    """Get all profiles."""
    try:
        profiles = profile_mgr.list_profiles()
        return jsonify({
            "success": True,
            "data": profiles,
            "count": len(profiles)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/profiles/<profile_name>', methods=['GET'])
def get_profile(profile_name):
    """Get a specific profile."""
    try:
        profile = profile_mgr.load_profile(profile_name)
        if not profile:
            return jsonify({
                "success": False,
                "error": "Profile not found"
            }), 404
        
        stats = profile_mgr.get_profile_stats(profile_name)
        progress_stats = progress_tracker.get_statistics(profile_name)
        
        return jsonify({
            "success": True,
            "data": {
                "profile": profile,
                "stats": stats,
                "progress": progress_stats
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/profiles/<profile_name>', methods=['PUT'])
def update_profile(profile_name):
    """Update a profile."""
    try:
        data = request.json
        profile = profile_mgr.update_profile(profile_name, data)
        
        if not profile:
            return jsonify({
                "success": False,
                "error": "Profile not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": profile
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/profiles/<profile_name>', methods=['DELETE'])
def delete_profile(profile_name):
    """Delete a profile."""
    try:
        success = profile_mgr.delete_profile(profile_name)
        
        if not success:
            return jsonify({
                "success": False,
                "error": "Profile not found"
            }), 404
        
        return jsonify({
            "success": True,
            "message": "Profile deleted successfully"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/profiles/<profile_name>/export', methods=['GET'])
def export_profile(profile_name):
    """Export a profile."""
    try:
        export_format = request.args.get('format', 'json')
        profile = profile_mgr.load_profile(profile_name)
        
        if not profile:
            return jsonify({
                "success": False,
                "error": "Profile not found"
            }), 404
        
        if export_format == 'json':
            return jsonify(profile)
        
        elif export_format == 'csv':
            # Return CSV format
            import csv
            from io import StringIO
            
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(profile.keys())
            writer.writerow(profile.values())
            
            return output.getvalue(), 200, {
                'Content-Type': 'text/csv',
                'Content-Disposition': f'attachment; filename={profile_name}.csv'
            }
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/profiles/<profile_name>/progress', methods=['GET'])
def get_profile_progress(profile_name):
    """Get progress log for a profile."""
    try:
        logs = progress_tracker.get_activity_log(profile_name)
        stats = progress_tracker.get_statistics(profile_name)
        
        return jsonify({
            "success": True,
            "data": {
                "logs": logs,
                "stats": stats
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/profiles/<profile_name>/progress', methods=['POST'])
def log_progress(profile_name):
    """Log progress for a profile."""
    try:
        data = request.json
        progress_tracker.log_activity(
            profile_name,
            data.get('type', 'activity'),
            data.get('details', {})
        )
        
        return jsonify({
            "success": True,
            "message": "Progress logged successfully"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_dashboard_stats():
    """Get overall dashboard statistics."""
    try:
        profiles = profile_mgr.list_profiles()
        total_profiles = len(profiles)
        
        total_activities = 0
        total_completed = 0
        
        for profile in profiles:
            stats = progress_tracker.get_statistics(profile.get('name', ''))
            total_activities += stats.get('total_activities', 0)
            # Count completed activities
            completed = stats.get('activity_types', {}).get('milestone_completed', 0)
            total_completed += completed
        
        return jsonify({
            "success": True,
            "data": {
                "total_profiles": total_profiles,
                "total_activities": total_activities,
                "total_completed": total_completed,
                "recent_profiles": profiles[:5]
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ── Error Handlers ─────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "success": False,
        "error": "Resource not found"
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  🚀 Career Assistant Web Dashboard                           ║
    ║  Starting Flask server on http://localhost:5000              ║
    ║  Press CTRL+C to stop                                         ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
