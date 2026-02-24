# Career Assistant Platform - Complete Feature Reference

## Table of Contents
1. [Module Overview](#module-overview)
2. [API Reference](#api-reference)
3. [Feature Matrix](#feature-matrix)
4. [Code Examples](#code-examples)
5. [Integration Guide](#integration-guide)

---

## Module Overview

### Architecture Diagram
```
┌─────────────────────────────────────────┐
│          app.py (Main Application)      │
│         7-Tab Streamlit Interface       │
└─────────────────────────────────────────┘
         ↓         ↓         ↓         ↓
    ┌────────┬──────────┬──────────┬─────────┐
    │ utils  │  storage │assessment│ reports │
    └────────┴──────────┴──────────┴─────────┘
         ↓         ↓         ↓         ↓
    ┌────────┬──────────┬──────────┬─────────┐
    │  llm   │ prompts  │vis.utils │  storage│
    └────────┴──────────┴──────────┴─────────┘
```

### Module Dependencies
```
Core Dependencies:
├── streamlit          Base framework
├── requests           HTTP requests
├── python-dotenv      Environment variables
├── huggingface_hub    LLM API access

Data & Analytics:
├── pandas             Data manipulation
├── numpy              Numerical computing
├── plotly             Interactive visualization
├── matplotlib         Static plotting

Export & Storage:
├── reportlab          PDF generation
├── pillow             Image processing
└── json              Built-in data serialization
```

---

## API Reference

### `utils/storage.py` - Data Persistence

#### `save_profile(profile_name, data)`
**Purpose**: Create or update a user profile  
**Parameters**:
- `profile_name` (str): Unique identifier for profile
- `data` (dict): Profile configuration dictionary

**Example**:
```python
from utils.storage import save_profile

config = {
    "career_field": "Machine Learning",
    "goal": "Senior ML Engineer at FAANG",
    "experience": "Intermediate",
    "created_at": "2026-02-24T10:30:00",
    "interests": ["Deep Learning", "NLP", "Computer Vision"],
    "target_salary": "$150k+",
    "timeline": "12 months"
}

save_profile("jane_ml_eng", config)
```

**Returns**: `None` (creates file in `data/profiles/`)  
**Errors**: `IOError` if file write fails

---

#### `load_profile(profile_name)`
**Purpose**: Retrieve a saved profile  
**Parameters**:
- `profile_name` (str): Profile identifier

**Example**:
```python
from utils.storage import load_profile

profile = load_profile("jane_ml_eng")
print(profile["career_field"])      # "Machine Learning"
print(profile["experience"])        # "Intermediate"
```

**Returns**: Dictionary with profile data  
**Errors**: `FileNotFoundError` if profile doesn't exist

---

#### `get_all_profiles()`
**Purpose**: List all saved profiles  
**Parameters**: None

**Example**:
```python
from utils.storage import get_all_profiles

profiles = get_all_profiles()
print(profiles)  # ["jane_ml_eng", "bob_dateng", "alice_webdev"]

for profile_name in profiles:
    profile = load_profile(profile_name)
    print(f"{profile_name}: {profile['career_field']}")
```

**Returns**: List of profile name strings  
**Errors**: Returns empty list if no profiles exist

---

#### `delete_profile(profile_name)`
**Purpose**: Remove a profile and all associated data  
**Parameters**:
- `profile_name` (str): Profile to delete

**Example**:
```python
from utils.storage import delete_profile

delete_profile("old_profile_name")
print("Profile deleted successfully")
```

**Returns**: `None`  
**Errors**: `FileNotFoundError` if profile doesn't exist

---

#### `save_roadmap(profile_name, roadmap_data)`
**Purpose**: Save a career roadmap to a profile  
**Parameters**:
- `profile_name` (str): Target profile
- `roadmap_data` (str or dict): Roadmap content

**Example**:
```python
from utils.storage import save_roadmap

roadmap = """
## 6-Month ML Engineer Roadmap
### Month 1-2: Foundations
- Deep Learning Theory
- TensorFlow/PyTorch
- Data Preprocessing

### Month 3-4: Advanced
- Model Architectures
- Transfer Learning
...
"""

save_roadmap("jane_ml_eng", roadmap)
```

**Returns**: `None`  
**Storage**: `data/results/`

---

#### `save_resume_analysis(profile_name, analysis)`
**Purpose**: Store resume feedback and recommendations  
**Parameters**:
- `profile_name` (str): Target profile
- `analysis` (str): AI-generated analysis

**Example**:
```python
from utils.storage import save_resume_analysis

analysis = """
RESUME REVIEW - Jane ML Engineer

STRENGTHS:
✓ Strong technical background
✓ Relevant project experience
✓ Clear career progression

AREAS FOR IMPROVEMENT:
• Add quantifiable impact metrics
• Highlight ML frameworks used
• Include research publications
...
"""

save_resume_analysis("jane_ml_eng", analysis)
```

**Returns**: `None`

---

#### `save_interview_session(profile_name, session_data)`
**Purpose**: Record interview practice session  
**Parameters**:
- `profile_name` (str): Target profile
- `session_data` (dict): Session details

**Example**:
```python
from utils.storage import save_interview_session
from datetime import datetime

session = {
    "type": "interview",
    "interview_type": "Behavioral",
    "role": "Senior ML Engineer",
    "timestamp": datetime.now().isoformat(),
    "questions_count": 3,
    "duration_minutes": 15,
    "questions": [
        {
            "question": "Tell me about a challenging project",
            "answer": "At my previous company...",
            "feedback": "Good structure, add more metrics"
        }
    ]
}

save_interview_session("jane_ml_eng", session)
```

**Returns**: `None`

---

#### `get_profile_stats(profile_name)`
**Purpose**: Generate statistics for a profile  
**Parameters**:
- `profile_name` (str): Profile to analyze

**Example**:
```python
from utils.storage import get_profile_stats

stats = get_profile_stats("jane_ml_eng")
print(stats)
# {
#     "chat_interactions": 15,
#     "assessments_completed": 3,
#     "interviews_practiced": 5,
#     "roadmaps_created": 1,
#     "resumes_analyzed": 2,
#     "last_updated": "2026-02-24T15:30:00"
# }
```

**Returns**: Dictionary with usage statistics

---

### `utils/assessment.py` - Skill Assessment

#### `get_available_topics()`
**Purpose**: List all available assessment topics  
**Parameters**: None

**Example**:
```python
from utils.assessment import get_available_topics

topics = get_available_topics()
print(topics)
# ['Python Fundamentals', 'SQL Basics', 'Data Analysis', 'Machine Learning']
```

**Returns**: List of topic strings

---

#### `get_assessment(topic, num_questions)`
**Purpose**: Retrieve assessment questions for a topic  
**Parameters**:
- `topic` (str): Assessment topic
- `num_questions` (int): Number of questions (1-10)

**Example**:
```python
from utils.assessment import get_assessment

assessment = get_assessment("Python Fundamentals", 5)
print(assessment)
# {
#     'questions': [
#         {
#             'question': 'What is a list in Python?',
#             'a': 'Ordered mutable collection',
#             'b': 'Unordered set of items',
#             'c': 'Fixed-size array',
#             'd': 'Dictionary-like structure'
#         },
#         ...
#     ],
#     'correct_answers': ['a', 'b', 'c', ...]
# }
```

**Returns**: Dictionary with questions and answers

---

#### `calculate_score(answers, correct_answers)`
**Purpose**: Score assessment answers  
**Parameters**:
- `answers` (dict): User's answers {0: 'a', 1: 'b', ...}
- `correct_answers` (list): Correct answers list

**Example**:
```python
from utils.assessment import calculate_score

user_answers = {0: 'a', 1: 'b', 2: 'c', 3: 'b', 4: 'a'}
correct = ['a', 'b', 'c', 'a', 'd']

score = calculate_score(user_answers, correct)
print(score)
# {
#     'correct': 4,
#     'total': 5,
#     'percentage': 80
# }
```

**Returns**: Dictionary with scoring details

---

#### `get_skill_level(percentage)`
**Purpose**: Convert percentage score to skill level  
**Parameters**:
- `percentage` (int): Score percentage (0-100)

**Example**:
```python
from utils.assessment import get_skill_level

levels = [get_skill_level(p) for p in [45, 65, 75, 85, 92]]
print(levels)
# ['Beginner', 'Intermediate', 'Proficient', 'Advanced', 'Expert']
```

**Returns**: Skill level string

---

### `utils/visualizations.py` - Analytics

#### `calculate_engagement_score(stats)`
**Purpose**: Calculate 0-100 engagement score  
**Parameters**:
- `stats` (dict): User activity statistics

**Example**:
```python
from utils.visualizations import calculate_engagement_score

stats = {
    "chat_interactions": 20,
    "assessments_completed": 4,
    "interviews_practiced": 3,
    "roadmaps_created": 1,
    "resumes_analyzed": 2
}

score = calculate_engagement_score(stats)
print(f"Engagement: {score}/100")  # Engagement: 78/100
```

**Formula**:
```
Score = (interactions × 0.4) + (roadmaps × 10) + (resumes × 15) + (interviews × 20)
Max: 100
```

**Returns**: Integer 0-100

---

#### `generate_progress_summary(stats)`
**Purpose**: Create text summary of user progress  
**Parameters**:
- `stats` (dict): User statistics

**Example**:
```python
from utils.visualizations import generate_progress_summary

summary = generate_progress_summary(stats)
print(summary)
# "You've had 20 interactions with your mentor.
#  Completed 4 skill assessments with avg score: 82%.
#  Next action: Practice technical interviews."
```

**Returns**: Text summary string

---

#### `get_next_recommended_action(stats)`
**Purpose**: Suggest next learning step based on progress  
**Parameters**:
- `stats` (dict): User statistics

**Example**:
```python
from utils.visualizations import get_next_recommended_action

action = get_next_recommended_action(stats)
print(action)  # "Complete your Machine Learning assessment"
```

**Returns**: Recommendation string

---

### `utils/reports.py` - Report Generation

#### `generate_text_report(profile_name, stats)`
**Purpose**: Create formatted text report  
**Parameters**:
- `profile_name` (str): Profile identifier
- `stats` (dict): Profile statistics

**Example**:
```python
from utils.reports import generate_text_report

report = generate_text_report("jane_ml_eng", stats)
with open("report.txt", "w") as f:
    f.write(report)
```

**Output Format**:
```
================================================================================
CAREER PROFILE REPORT
================================================================================

Profile: jane_ml_eng
Generated: 2026-02-24 15:30:00
Career Field: Machine Learning
Experience Level: Intermediate

[Detailed metrics and analysis...]
```

**Returns**: Formatted text string

---

#### `generate_csv_export(profile_names)`
**Purpose**: Export profiles as CSV  
**Parameters**:
- `profile_names` (list): List of profile identifiers

**Example**:
```python
from utils.reports import generate_csv_export

profiles = ["jane_ml_eng", "bob_dateng", "alice_webdev"]
csv_data = generate_csv_export(profiles)

with open("profiles.csv", "w") as f:
    f.write(csv_data)
```

**CSV Columns**:
```
Profile,Field,Goal,Experience,Engagement,Last_Updated
jane_ml_eng,Machine Learning,...,Intermediate,78,2026-02-24
```

**Returns**: CSV-formatted string

---

#### `generate_json_export(profile_names)`
**Purpose**: Export profiles as JSON  
**Parameters**:
- `profile_names` (list): List of profile identifiers

**Example**:
```python
from utils.reports import generate_json_export
import json

profiles = ["jane_ml_eng", "bob_dateng"]
json_data = generate_json_export(profiles)

data = json.loads(json_data)
print(data["profiles"][0]["career_field"])
```

**JSON Structure**:
```json
{
    "export_date": "2026-02-24T15:30:00",
    "profiles": [
        {
            "name": "jane_ml_eng",
            "career_field": "Machine Learning",
            "experience": "Intermediate",
            "stats": {...}
        }
    ]
}
```

**Returns**: JSON-formatted string

---

#### `generate_summary_stats(profile_names)`
**Purpose**: Generate system-wide statistics  
**Parameters**:
- `profile_names` (list): List of profile identifiers

**Example**:
```python
from utils.reports import generate_summary_stats

summary = generate_summary_stats(["jane_ml_eng", "bob_dateng"])
print(summary)
# {
#     'total_profiles': 2,
#     'avg_engagement': 72.5,
#     'total_interactions': 35,
#     'active_assessments': 7
# }
```

**Returns**: Dictionary with aggregated statistics

---

## Feature Matrix

| Feature | Module | File | Status | Integration |
|---------|--------|------|--------|-------------|
| Profile Management | storage | storage.py | ✅ Complete | app.py sidebar |
| Data Persistence | storage | storage.py | ✅ Complete | All tabs |
| Chat History | storage | storage.py | ✅ Complete | Tab 2 |
| Roadmap Storage | storage | storage.py | ✅ Complete | Tab 1 |
| Resume Analysis | storage | storage.py | ✅ Complete | Tab 4 |
| Interview Recording | storage | storage.py | ✅ Complete | Tab 5 |
| Skill Assessment | assessment | assessment.py | ✅ Complete | Tab 6 |
| Score Calculation | assessment | assessment.py | ✅ Complete | Tab 6 |
| Engagement Tracking | visualizations | visualizations.py | ✅ Complete | Tab 7 |
| Progress Recommendations | visualizations | visualizations.py | ✅ Complete | Tab 7 |
| Text Report Export | reports | reports.py | ✅ Complete | Tab 7 |
| CSV Export | reports | reports.py | ✅ Complete | Tab 7 |
| JSON Export | reports | reports.py | ✅ Complete | Tab 7 |
| LLM Integration | llm | llm.py | ✅ Complete | Tabs 1-5 |
| Prompt Templates | prompts | prompts.py | ✅ Complete | Tabs 1-5 |

---

## Code Examples

### Example 1: Complete Assessment Workflow
```python
from utils.assessment import get_assessment, calculate_score, get_skill_level

# 1. Get assessment
topic = "Python Fundamentals"
assessment = get_assessment(topic, 5)

# 2. User answers (in real app, from UI)
user_answers = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'a'}

# 3. Calculate score
score = calculate_score(user_answers, assessment['correct_answers'])

# 4. Get skill level
level = get_skill_level(score['percentage'])

# 5. Save to profile
from utils.storage import save_profile
profile_data = {
    "assessment_scores": {
        topic: {
            "percentage": score['percentage'],
            "level": level
        }
    }
}
save_profile("user_001", profile_data)
```

### Example 2: Generate and Export Report
```python
from utils.storage import get_profile_stats, get_all_profiles
from utils.reports import generate_text_report, generate_csv_export

# Get all profiles
profiles = get_all_profiles()

# Generate reports
for profile in profiles:
    stats = get_profile_stats(profile)
    report = generate_text_report(profile, stats)
    
    # Save individual report
    with open(f"{profile}_report.txt", "w") as f:
        f.write(report)

# Generate combined CSV
csv = generate_csv_export(profiles)
with open("all_profiles.csv", "w") as f:
    f.write(csv)
```

### Example 3: Track User Progress
```python
from utils.storage import get_profile_stats
from utils.visualizations import (
    calculate_engagement_score,
    generate_progress_summary,
    get_next_recommended_action
)

profile = "jane_career"
stats = get_profile_stats(profile)

# Calculate metrics
engagement = calculate_engagement_score(stats)
summary = generate_progress_summary(stats)
next_action = get_next_recommended_action(stats)

# Display
print(f"Engagement: {engagement}/100")
print(f"Summary: {summary}")
print(f"Recommendation: {next_action}")
```

---

## Integration Guide

### Adding a New Feature

#### Step 1: Create utility module
```python
# utils/new_feature.py
def feature_function(param1, param2):
    """Description"""
    return result
```

#### Step 2: Import in app.py
```python
from utils.new_feature import feature_function
```

#### Step 3: Use in appropriate tab
```python
with tab_x:
    st.header("Feature Name")
    result = feature_function(param1, param2)
    st.write(result)
```

#### Step 4: Integrate with storage (if needed)
```python
save_profile(profile_name, {**profile_data, "new_data": result})
```

### Connecting to LLM

```python
from utils.llm import query_model

system_prompt = "You are an expert in X field"
user_prompt = "Tell me about Y"

response = query_model(system_prompt, user_prompt, max_tokens=1500)
st.write(response)
```

---

## Performance Optimization

### Caching Profile Data
```python
import streamlit as st
from utils.storage import load_profile

@st.cache_data
def get_cached_profile(name):
    return load_profile(name)

profile = get_cached_profile("user_001")
```

### Batch Processing
```python
from utils.storage import get_all_profiles, get_profile_stats

profiles = get_all_profiles()
stats = {p: get_profile_stats(p) for p in profiles}
```

---

## Deployment Considerations

### Environment Variables
```bash
# .env file
HUGGINGFACE_API_KEY=hf_xxxxxx
LOG_LEVEL=INFO
MAX_TOKENS=2000
```

### Error Handling
```python
try:
    profile = load_profile("unknown")
except FileNotFoundError:
    st.error("Profile not found")
```

---

**API Version**: 2.0  
**Last Updated**: February 24, 2026  
**Stability**: Production Ready
