# ============================================================================
# ASSESSMENT & SKILL TESTS
# ============================================================================
# Provides skill assessment tests, scoring, and evaluation

import random
from typing import List, Dict, Tuple

# ============================================================================
# SKILL ASSESSMENT TESTS
# ============================================================================

ASSESSMENT_QUESTIONS = {
    "Python Fundamentals": [
        {
            "question": "What is the output of: print(len({1, 2, 2, 3, 3, 3}))",
            "options": ["3", "6", "Error", "Undefined"],
            "correct": 0,
            "explanation": "Sets remove duplicates, so {1,2,2,3,3,3} becomes {1,2,3} with len=3"
        },
        {
            "question": "Which of these is a mutable data type in Python?",
            "options": ["Tuple", "String", "List", "Integer"],
            "correct": 2,
            "explanation": "Lists are mutable; tuples, strings, and integers are immutable"
        },
        {
            "question": "What does *args do in a function definition?",
            "options": ["Stores keyword arguments", "Stores multiple positional arguments", "Stores named arguments", "None"],
            "correct": 1,
            "explanation": "*args allows a function to accept variable number of positional arguments"
        },
        {
            "question": "What is the difference between == and 'is'?",
            "options": ["No difference", "== checks equality, is checks identity", "is checks equality", "They are opposite"],
            "correct": 1,
            "explanation": "== compares values, is compares object identity (memory address)"
        },
        {
            "question": "What will be the output? x = [1,2,3]; x.append([4,5]); print(len(x))",
            "options": ["4", "5", "Error", "6"],
            "correct": 0,
            "explanation": "append adds one element (the list [4,5]), so length becomes 4"
        }
    ],
    "SQL Basics": [
        {
            "question": "What does SQL stand for?",
            "options": ["Structured Query Language", "Simple Query Language", "Standard Query Language", "System Query Language"],
            "correct": 0,
            "explanation": "SQL stands for Structured Query Language"
        },
        {
            "question": "Which SQL clause filters records after GROUP BY?",
            "options": ["WHERE", "HAVING", "FILTER", "GROUP"],
            "correct": 1,
            "explanation": "WHERE filters before grouping, HAVING filters after GROUP BY"
        },
        {
            "question": "What is a PRIMARY KEY?",
            "options": ["First column", "Unique identifier for each row", "Main table", "Foreign key"],
            "correct": 1,
            "explanation": "PRIMARY KEY uniquely identifies each record in a table"
        },
        {
            "question": "What does a JOIN do?",
            "options": ["Combines data from multiple tables", "Joins strings", "Links to external database", "Creates backup"],
            "correct": 0,
            "explanation": "JOIN combines columns from two or more tables based on a condition"
        },
        {
            "question": "What keyword prevents duplicate rows in results?",
            "options": ["UNIQUE", "DISTINCT", "DIFFERENT", "REMOVE"],
            "correct": 1,
            "explanation": "DISTINCT removes duplicate rows from query results"
        }
    ],
    "Data Analysis": [
        {
            "question": "What does EDA stand for?",
            "options": ["Exploratory Data Analysis", "Experimental Data Algorithm", "External Data Access", "Electronic Data Arrangement"],
            "correct": 0,
            "explanation": "EDA is Exploratory Data Analysis"
        },
        {
            "question": "Which is NOT a measure of central tendency?",
            "options": ["Mean", "Median", "Mode", "Range"],
            "correct": 3,
            "explanation": "Range is a measure of dispersion, not central tendency"
        },
        {
            "question": "What does a correlation coefficient of -0.8 indicate?",
            "options": ["Strong positive correlation", "Weak negative correlation", "Strong negative correlation", "No correlation"],
            "correct": 2,
            "explanation": "A coefficient near -1 indicates strong negative correlation"
        },
        {
            "question": "What is the purpose of normalization?",
            "options": ["Delete data", "Scale features to similar range", "Remove duplicates", "Convert format"],
            "correct": 1,
            "explanation": "Normalization scales features to a similar range for better ML performance"
        },
        {
            "question": "What percentage of data should typically be in training set?",
            "options": ["50%", "70%", "90%", "100%"],
            "correct": 1,
            "explanation": "Common practice is 70-80% for training, 20-30% for testing"
        }
    ],
    "Machine Learning": [
        {
            "question": "What is overfitting?",
            "options": ["Model too simple", "Model learns training data too well", "Model has too many parameters", "Both B and C"],
            "correct": 3,
            "explanation": "Overfitting occurs when model is too complex and learns noise; typically has too many parameters"
        },
        {
            "question": "Which metric is best for imbalanced datasets?",
            "options": ["Accuracy", "Precision", "F1-Score", "MAE"],
            "correct": 2,
            "explanation": "F1-Score is better for imbalanced data as it balances precision and recall"
        },
        {
            "question": "What does cross-validation do?",
            "options": ["Tests on different data splits", "Validates across countries", "Checks model complexity", "Verifies features"],
            "correct": 0,
            "explanation": "Cross-validation evaluates model performance across multiple data splits"
        },
        {
            "question": "Which is a supervised learning algorithm?",
            "options": ["K-Means", "PCA", "Random Forest", "DBSCAN"],
            "correct": 2,
            "explanation": "Random Forest is supervised; K-Means and DBSCAN are unsupervised"
        },
        {
            "question": "What is feature engineering?",
            "options": ["Building ML model", "Creating new features from raw data", "Selecting algorithms", "Tuning hyperparameters"],
            "correct": 1,
            "explanation": "Feature engineering is creating meaningful features from raw data"
        }
    ]
}

# ============================================================================
# SCORE CALCULATION
# ============================================================================

def calculate_score(answers: List[int], correct_answers: List[int]) -> Dict:
    """
    Calculate assessment score
    
    Args:
        answers: List of selected answer indices
        correct_answers: List of correct answer indices
    
    Returns:
        Dictionary with score, percentage, and feedback
    """
    if len(answers) != len(correct_answers):
        return {"error": "Answer count mismatch"}
    
    correct_count = sum(1 for a, c in zip(answers, correct_answers) if a == c)
    total = len(answers)
    percentage = (correct_count / total) * 100
    
    # Performance level
    if percentage >= 90:
        level = "Expert"
        feedback = "Excellent! You demonstrate strong mastery of this topic."
    elif percentage >= 80:
        level = "Advanced"
        feedback = "Great job! You have solid understanding with minor gaps."
    elif percentage >= 70:
        level = "Proficient"
        feedback = "Good foundation! Continue practicing to improve further."
    elif percentage >= 60:
        level = "Intermediate"
        feedback = "You have basic knowledge. Focus on weak areas."
    else:
        level = "Beginner"
        feedback = "Keep practicing! This topic needs more attention."
    
    return {
        "correct": correct_count,
        "total": total,
        "percentage": round(percentage, 2),
        "level": level,
        "feedback": feedback
    }

def get_skill_level(percentage: float) -> str:
    """Get skill level based on percentage"""
    if percentage >= 90:
        return "Expert (90+%)"
    elif percentage >= 80:
        return "Advanced (80-89%)"
    elif percentage >= 70:
        return "Proficient (70-79%)"
    elif percentage >= 60:
        return "Intermediate (60-69%)"
    else:
        return "Beginner (<60%)"

# ============================================================================
# READINESS SCORING
# ============================================================================

def calculate_role_readiness(assessment_scores: Dict[str, float]) -> Dict:
    """
    Calculate overall role readiness based on skill assessments
    
    Args:
        assessment_scores: Dictionary of skill -> percentage score
    
    Returns:
        Overall readiness score and breakdown
    """
    if not assessment_scores:
        return {"overall_score": 0, "status": "No assessments taken"}
    
    scores = list(assessment_scores.values())
    overall = sum(scores) / len(scores)
    
    if overall >= 85:
        status = "🟢 Role Ready - Interview Preparation Recommended"
    elif overall >= 70:
        status = "🟡 Preparation Needed - Focus on weak areas"
    elif overall >= 50:
        status = "🔴 More Learning Required - Substantial gaps identified"
    else:
        status = "🔴 Beginner Level - Start with fundamentals"
    
    return {
        "overall_score": round(overall, 2),
        "status": status,
        "breakdown": assessment_scores
    }

# ============================================================================
# INTERVIEW SCORING
# ============================================================================

def score_interview_answer(answer_length: int, emotional_tone: str = "neutral") -> Dict:
    """
    Score an interview answer
    
    Args:
        answer_length: Length of answer in characters
        emotional_tone: Quality tone (poor, average, good, excellent)
    
    Returns:
        Score and feedback
    """
    # Length score (25 points)
    if answer_length < 100:
        length_score = 5
        length_feedback = "Too brief - expand with more details"
    elif answer_length < 300:
        length_score = 15
        length_feedback = "Good length for most questions"
    elif answer_length < 600:
        length_score = 25
        length_feedback = "Excellent comprehensive answer"
    else:
        length_score = 20
        length_feedback = "A bit long - conciseness is important"
    
    # Tone score (25 points)
    tone_scores = {
        "poor": (5, "Unclear or rambling"),
        "average": (15, "Adequate but could be clearer"),
        "good": (22, "Clear and well-structured"),
        "excellent": (25, "Excellent clarity and delivery")
    }
    tone_score, tone_feedback = tone_scores.get(emotional_tone, (15, "Neutral"))
    
    # Structure score (50 points) - based on STAR method presence
    # This would be calculated based on actual answer analysis
    structure_score = 30  # Default
    
    total_score = length_score + tone_score + structure_score
    
    return {
        "total_score": total_score,
        "max_score": 100,
        "percentage": (total_score / 100) * 100,
        "breakdown": {
            "length": {"score": length_score, "feedback": length_feedback},
            "tone": {"score": tone_score, "feedback": tone_feedback},
            "structure": {"score": structure_score, "feedback": "Consider using STAR method"}
        }
    }

# ============================================================================
# ASSESSMENT RETRIEVAL
# ============================================================================

def get_assessment(topic: str, num_questions: int = 5) -> Tuple[List[Dict], List[int]]:
    """
    Get assessment questions for a topic
    
    Args:
        topic: Assessment topic
        num_questions: Number of questions to return
    
    Returns:
        Tuple of (questions list, correct answers list)
    """
    if topic not in ASSESSMENT_QUESTIONS:
        return [], []
    
    questions = ASSESSMENT_QUESTIONS[topic]
    selected = random.sample(questions, min(num_questions, len(questions)))
    
    questions_list = []
    correct_answers = []
    
    for q in selected:
        questions_list.append({
            "question": q["question"],
            "options": q["options"],
            "explanation": q["explanation"]
        })
        correct_answers.append(q["correct"])
    
    return questions_list, correct_answers

def get_available_topics() -> List[str]:
    """Get list of available assessment topics"""
    return list(ASSESSMENT_QUESTIONS.keys())
