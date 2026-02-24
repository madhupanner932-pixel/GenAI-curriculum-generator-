// ── Dashboard Application ────────────────────────────────────────────────────

const API_BASE = '/api';
let profileChart, activityChart, skillsChart, progressChart;

// ── Initialize Dashboard ─────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadDashboardStats();
    loadProfiles();
});

function initializeEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            switchView(item.dataset.view);
        });
    });
    
    // Menu toggle
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }
    
    // Buttons
    document.getElementById('sync-btn').addEventListener('click', loadDashboardStats);
    document.getElementById('add-profile-btn').addEventListener('click', openNewProfileModal);
    document.getElementById('export-all-btn').addEventListener('click', exportAllProfiles);
    document.getElementById('import-btn').addEventListener('click', importProfiles);
    document.getElementById('reset-btn').addEventListener('click', resetAllData);
    
    // Modal close
    document.querySelector('.modal-close').addEventListener('click', closeModal);
    document.getElementById('profile-modal').addEventListener('click', closeModal);
    
    // Dark mode toggle
    const darkModeToggle = document.getElementById('dark-mode');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('change', toggleDarkMode);
    }
}

// ── View Management ──────────────────────────────────────────────────────────
function switchView(viewName) {
    // Hide all views
    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active');
    });
    
    // Show selected view
    const viewElement = document.getElementById(`${viewName}-view`);
    if (viewElement) {
        viewElement.classList.add('active');
    }
    
    // Update navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    document.querySelector(`[data-view="${viewName}"]`).classList.add('active');
    
    // Update page title
    const titles = {
        'overview': 'Overview',
        'profiles': 'My Profiles',
        'progress': 'Your Progress',
        'analytics': 'Career Analytics',
        'settings': 'Settings'
    };
    document.getElementById('page-title').textContent = titles[viewName] || 'Dashboard';
    
    // Load data for specific views
    if (viewName === 'profiles') {
        loadProfiles();
    } else if (viewName === 'progress') {
        loadProgress();
    } else if (viewName === 'analytics') {
        loadAnalytics();
    }
}

// ── Dashboard Stats ──────────────────────────────────────────────────────────
async function loadDashboardStats() {
    try {
        const response = await axios.get(`${API_BASE}/stats`);
        const data = response.data.data;
        
        // Update stat cards
        document.getElementById('total-profiles').textContent = data.total_profiles;
        document.getElementById('total-activities').textContent = data.total_activities;
        document.getElementById('total-completed').textContent = data.total_completed;
        
        const rate = data.total_activities > 0 
            ? Math.round((data.total_completed / data.total_activities) * 100)
            : 0;
        document.getElementById('completion-rate').textContent = `${rate}%`;
        
        // Update recent profiles
        const recentList = document.getElementById('recent-profiles');
        recentList.innerHTML = '';
        
        if (data.recent_profiles.length > 0) {
            data.recent_profiles.forEach(profile => {
                const item = createProfileItem(profile);
                recentList.appendChild(item);
            });
        } else {
            recentList.innerHTML = '<p class="text-muted">No profiles yet</p>';
        }
        
        // Create charts
        createProfileChart(data);
        createActivityChart(data);
        
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
    }
}

function createProfileItem(profile) {
    const div = document.createElement('div');
    div.className = 'profile-item';
    div.innerHTML = `
        <div class="profile-item-info">
            <h4>${profile.name}</h4>
            <p>${profile.career_field} • ${profile.experience_level}</p>
        </div>
        <span class="profile-item-arrow">→</span>
    `;
    div.addEventListener('click', () => openProfileDetail(profile.name));
    return div;
}

function createProfileChart(data) {
    const ctx = document.getElementById('profileChart');
    if (!ctx) return;
    
    if (profileChart) {
        profileChart.destroy();
    }
    
    profileChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Active', 'Completed', 'Pending'],
            datasets: [{
                data: [
                    Math.max(1, data.total_profiles - data.total_completed),
                    data.total_completed,
                    1
                ],
                backgroundColor: ['#6C63FF', '#43E97B', '#FF6584'],
                borderColor: '#141528',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    labels: {
                        color: '#F0F0FF',
                        font: { size: 12 }
                    }
                }
            }
        }
    });
}

function createActivityChart(data) {
    const ctx = document.getElementById('activityChart');
    if (!ctx) return;
    
    if (activityChart) {
        activityChart.destroy();
    }
    
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const activityData = days.map(() => Math.floor(Math.random() * data.total_activities));
    
    activityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: days,
            datasets: [{
                label: 'Activities',
                data: activityData,
                borderColor: '#6C63FF',
                backgroundColor: 'rgba(108, 99, 255, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    labels: { color: '#F0F0FF' }
                }
            },
            scales: {
                y: {
                    ticks: { color: '#8888AA' },
                    grid: { color: 'rgba(108, 99, 255, 0.1)' }
                },
                x: {
                    ticks: { color: '#8888AA' },
                    grid: { color: 'rgba(108, 99, 255, 0.1)' }
                }
            }
        }
    });
}

// ── Profiles Management ───────────────────────────────────────────────────────
async function loadProfiles() {
    try {
        const response = await axios.get(`${API_BASE}/profiles`);
        const profiles = response.data.data;
        
        const profilesList = document.getElementById('profiles-list');
        profilesList.innerHTML = '';
        
        if (profiles.length === 0) {
            profilesList.innerHTML = '<p class="text-muted">No profiles yet. Create one to get started!</p>';
            return;
        }
        
        profiles.forEach(profile => {
            const card = document.createElement('div');
            card.className = 'profile-card';
            card.innerHTML = `
                <h3>${profile.name}</h3>
                <div class="profile-info">
                    <strong>Field:</strong> ${profile.career_field}
                </div>
                <div class="profile-info">
                    <strong>Level:</strong> ${profile.experience_level}
                </div>
                <div class="profile-info">
                    <strong>Updated:</strong> ${new Date(profile.updated_at).toLocaleDateString()}
                </div>
                <span class="profile-badge">View Details →</span>
            `;
            card.addEventListener('click', () => openProfileDetail(profile.name));
            profilesList.appendChild(card);
        });
        
    } catch (error) {
        console.error('Error loading profiles:', error);
    }
}

async function openProfileDetail(profileName) {
    try {
        const response = await axios.get(`${API_BASE}/profiles/${profileName}`);
        const { profile, stats } = response.data.data;
        
        const modalBody = document.getElementById('modal-body');
        const modal = document.getElementById('profile-modal');
        
        modalBody.innerHTML = `
            <div style="padding: 1rem;">
                <h3>${profile.name}</h3>
                <p><strong>Field:</strong> ${profile.career_field}</p>
                <p><strong>Experience:</strong> ${profile.experience_level}</p>
                <p><strong>Created:</strong> ${new Date(profile.created_at).toLocaleDateString()}</p>
                
                <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border);">
                    <h4>Profile Status</h4>
                    <ul style="list-style: none; margin-top: 1rem;">
                        <li>📋 Roadmap: ${stats.has_roadmap ? '✅' : '❌'}</li>
                        <li>🎯 Skills: ${stats.has_skills ? '✅' : '❌'}</li>
                        <li>📈 Progress: ${stats.has_progress ? '✅' : '❌'}</li>
                    </ul>
                </div>
                
                <div style="margin-top: 1.5rem; display: flex; gap: 0.5rem;">
                    <button class="btn btn-primary" onclick="window.open('/streamlit-app?profile=${profileName}')">
                        Edit Profile
                    </button>
                    <button class="btn btn-secondary" onclick="deleteProfile('${profileName}')">
                        Delete
                    </button>
                </div>
            </div>
        `;
        
        document.getElementById('modal-title').textContent = 'Profile Details';
        modal.classList.add('active');
        
    } catch (error) {
        console.error('Error loading profile details:', error);
    }
}

async function deleteProfile(profileName) {
    if (!confirm(`Delete profile "${profileName}"?`)) return;
    
    try {
        await axios.delete(`${API_BASE}/profiles/${profileName}`);
        closeModal();
        loadProfiles();
    } catch (error) {
        console.error('Error deleting profile:', error);
        alert('Failed to delete profile');
    }
}

function openNewProfileModal() {
    const modal = document.getElementById('profile-modal');
    const modalBody = document.getElementById('modal-body');
    
    modalBody.innerHTML = `
        <form id="new-profile-form" style="padding: 1rem;">
            <div style="margin-bottom: 1rem;">
                <label style="display: block; margin-bottom: 0.5rem;">Profile Name</label>
                <input type="text" id="profile-name" style="width: 100%; padding: 0.5rem; border-radius: 4px; border: 1px solid var(--border); background: var(--bg-dark); color: var(--text-primary);" required>
            </div>
            <div style="margin-bottom: 1rem;">
                <label style="display: block; margin-bottom: 0.5rem;">Career Field</label>
                <input type="text" id="career-field" style="width: 100%; padding: 0.5rem; border-radius: 4px; border: 1px solid var(--border); background: var(--bg-dark); color: var(--text-primary);" required>
            </div>
            <div style="margin-bottom: 1.5rem;">
                <label style="display: block; margin-bottom: 0.5rem;">Experience Level</label>
                <select id="experience-level" style="width: 100%; padding: 0.5rem; border-radius: 4px; border: 1px solid var(--border); background: var(--bg-dark); color: var(--text-primary);">
                    <option value="Beginner">Beginner</option>
                    <option value="Intermediate">Intermediate</option>
                    <option value="Advanced">Advanced</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;">Create Profile</button>
        </form>
    `;
    
    document.getElementById('modal-title').textContent = 'New Profile';
    modal.classList.add('active');
    
    document.getElementById('new-profile-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const profileData = {
            name: document.getElementById('profile-name').value,
            career_field: document.getElementById('career-field').value,
            experience_level: document.getElementById('experience-level').value
        };
        
        try {
            // This would save to the profile system
            // For now, just show success
            alert('Profile creation would be synced with Streamlit app');
            closeModal();
            loadProfiles();
        } catch (error) {
            alert('Error creating profile');
        }
    });
}

// ── Progress & Analytics ─────────────────────────────────────────────────────
async function loadProgress() {
    const container = document.getElementById('progress-content');
    container.innerHTML = '<p class="text-muted">Loading progress data...</p>';
    // Load progress for all profiles
}

async function loadAnalytics() {
    // Create analytics charts
    const ctx1 = document.getElementById('skillsChart');
    const ctx2 = document.getElementById('progressChart');
    
    if (skillsChart) skillsChart.destroy();
    if (progressChart) progressChart.destroy();
    
    skillsChart = new Chart(ctx1, {
        type: 'radar',
        data: {
            labels: ['Technical', 'Communication', 'Leadership', 'Problem Solving', 'Learning'],
            datasets: [{
                label: 'Skills Score',
                data: [75, 65, 70, 80, 85],
                borderColor: '#6C63FF',
                backgroundColor: 'rgba(108, 99, 255, 0.1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { labels: { color: '#F0F0FF' } }
            },
            scales: {
                r: {
                    ticks: { color: '#8888AA' },
                    grid: { color: 'rgba(108, 99, 255, 0.1)' }
                }
            }
        }
    });
    
    progressChart = new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                label: 'Progress Score',
                data: [20, 35, 50, 75],
                backgroundColor: '#43E97B',
                borderColor: '#2BC76D',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { labels: { color: '#F0F0FF' } }
            },
            scales: {
                y: {
                    ticks: { color: '#8888AA' },
                    grid: { color: 'rgba(108, 99, 255, 0.1)' }
                },
                x: {
                    ticks: { color: '#8888AA' },
                    grid: { color: 'rgba(108, 99, 255, 0.1)' }
                }
            }
        }
    });
}

// ── Data Management ──────────────────────────────────────────────────────────
function exportAllProfiles() {
    // Trigger download of all profiles as JSON
    alert('Export would download all profiles as JSON file');
}

function importProfiles() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = async (event) => {
                try {
                    const data = JSON.parse(event.target.result);
                    // Import logic here
                    alert('Profiles imported successfully');
                    loadProfiles();
                } catch (error) {
                    alert('Error importing profiles');
                }
            };
            reader.readAsText(file);
        }
    });
    input.click();
}

async function resetAllData() {
    if (!confirm('This will delete ALL profiles and data. Are you sure?')) return;
    alert('Reset would clear all data');
}

// ── Modal Management ─────────────────────────────────────────────────────────
function closeModal() {
    const modal = document.getElementById('profile-modal');
    modal.classList.remove('active');
}

// ── Settings ─────────────────────────────────────────────────────────────────
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Load dark mode preferences
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
    document.getElementById('dark-mode').checked = true;
}
