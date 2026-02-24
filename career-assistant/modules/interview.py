"""
modules/interview.py

Mock Interview Simulator module — Streamlit UI + logic.
"""

import streamlit as st
from utils.model import query_model
from prompts.interview_prompt import (
    INTERVIEW_QUESTION_SYSTEM_PROMPT,
    INTERVIEW_EVAL_SYSTEM_PROMPT,
    INTERVIEW_SUMMARY_SYSTEM_PROMPT,
    get_interview_question_prompt,
    get_interview_eval_prompt,
    get_interview_summary_prompt,
)


QUESTION_TYPES = [
    "Technical / Conceptual",
    "Coding / Problem Solving",
    "Behavioral (STAR format)",
    "System Design",
    "Situational",
    "Role-Specific / Domain Knowledge",
]

MAX_QUESTIONS = 5  # Questions per session


def _extract_score(eval_text: str) -> int:
    """Try to extract the numeric score from evaluation text."""
    import re
    match = re.search(r"Score[:\s]*(\d+)/10", eval_text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 0


def render_interview():
    """Render the Mock Interview Simulator page."""

    # ── Session State Init ────────────────────────────────────────────────────
    if "interview_session" not in st.session_state:
        st.session_state["interview_session"] = []      # List of Q/A/score dicts
    if "current_question" not in st.session_state:
        st.session_state["current_question"] = None
    if "interview_active" not in st.session_state:
        st.session_state["interview_active"] = False
    if "awaiting_answer" not in st.session_state:
        st.session_state["awaiting_answer"] = False
    if "show_summary" not in st.session_state:
        st.session_state["show_summary"] = False
    if "interview_role" not in st.session_state:
        st.session_state["interview_role"] = ""

    # ── Header ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="module-header">
        <span class="module-icon">🎤</span>
        <div>
            <h2>Mock Interview Simulator</h2>
            <p>Practice real interview questions, get evaluated, and improve with expert feedback.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Summary View ──────────────────────────────────────────────────────────
    if st.session_state["show_summary"]:
        _render_summary()
        return

    # ── Setup Screen (not yet active) ─────────────────────────────────────────
    if not st.session_state["interview_active"]:
        _render_setup()
        return

    # ── Active Interview ──────────────────────────────────────────────────────
    _render_active_interview()


# ── Sub-renderers ─────────────────────────────────────────────────────────────

def _render_setup():
    """Show the interview setup form."""
    st.markdown("### ⚙️ Setup Your Mock Interview")

    with st.form("interview_setup"):
        col1, col2 = st.columns(2)
        with col1:
            role = st.text_input(
                "🎯 Target Role / Domain",
                placeholder="e.g. Data Analyst, Software Engineer, Product Manager...",
            )
        with col2:
            q_types = st.multiselect(
                "🎲 Question Types",
                QUESTION_TYPES,
                default=["Technical / Conceptual", "Behavioral (STAR format)"],
                help=f"Select the types of questions. {MAX_QUESTIONS} questions total."
            )

        start = st.form_submit_button(
            f"🎤 Start Mock Interview ({MAX_QUESTIONS} Questions)",
            use_container_width=True,
            type="primary"
        )

    if start:
        if not role.strip():
            st.error("⚠️ Please enter your target role.")
            return
        if not q_types:
            st.error("⚠️ Please select at least one question type.")
            return

        # Store setup and begin
        st.session_state["interview_role"] = role.strip()
        st.session_state["interview_q_types"] = q_types
        st.session_state["interview_session"] = []
        st.session_state["interview_active"] = True
        st.session_state["awaiting_answer"] = False
        st.session_state["show_summary"] = False
        st.session_state["current_question"] = None
        st.rerun()

    # Tips
    st.markdown("""
    <div class="tips-box">
        <h4>🎯 Tips for a Productive Mock Interview</h4>
        <ul>
            <li>Answer as if in a real interview — complete answers, not bullet notes.</li>
            <li>For behavioral questions, use the <strong>STAR format</strong>
                (Situation, Task, Action, Result).</li>
            <li>Take your time to think before answering — that's normal!</li>
            <li>Review feedback after each question to improve immediately.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


def _render_active_interview():
    """Run the interactive interview loop."""
    session        = st.session_state["interview_session"]
    role           = st.session_state["interview_role"]
    q_types        = st.session_state.get("interview_q_types", QUESTION_TYPES)
    q_num          = len(session) + 1
    total_q        = MAX_QUESTIONS

    # ── Progress bar ──────────────────────────────────────────────────────────
    progress = len(session) / total_q
    st.markdown(f"**Progress: Question {min(q_num, total_q)}/{total_q}**")
    st.progress(progress)
    st.markdown(f"🎯 Role: **{role}**")
    st.markdown("---")

    # ── Show past Q&As ────────────────────────────────────────────────────────
    for i, item in enumerate(session):
        with st.expander(f"✅ Q{i+1}: {item['question'][:80]}... | Score: {item['score']}/10", expanded=False):
            st.markdown(f"**Your Answer:** {item['answer']}")
            st.markdown("---")
            st.markdown(item["feedback"])

    # ── Check if interview is complete ────────────────────────────────────────
    if len(session) >= total_q:
        st.success(f"🎉 Interview complete! You answered all {total_q} questions.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 View Full Performance Summary", use_container_width=True, type="primary"):
                st.session_state["show_summary"] = True
                st.rerun()
        with col2:
            if st.button("🔄 Start New Interview", use_container_width=True):
                _reset_interview()
                st.rerun()
        return

    # ── Generate question if not yet asked ────────────────────────────────────
    if not st.session_state["awaiting_answer"]:
        # Pick a question type (cycle through selected types)
        q_type = q_types[(q_num - 1) % len(q_types)]

        with st.spinner(f"🤖 Preparing question {q_num}..."):
            user_prompt = get_interview_question_prompt(role, q_type, q_num)
            question = query_model(INTERVIEW_QUESTION_SYSTEM_PROMPT, user_prompt)

        st.session_state["current_question"] = question
        st.session_state["current_q_type"]   = q_type
        st.session_state["awaiting_answer"]   = True
        st.rerun()

    # ── Display current question & answer box ─────────────────────────────────
    current_q  = st.session_state["current_question"]
    current_qt = st.session_state.get("current_q_type", "")

    st.markdown(f"""
    <div class="question-card">
        <div class="q-type-badge">{current_qt}</div>
        <h3>Question {q_num}</h3>
        <p class="question-text">{current_q}</p>
    </div>
    """, unsafe_allow_html=True)

    answer = st.text_area(
        "✍️ Your Answer",
        height=200,
        placeholder="Type your answer here. Be as detailed and specific as you would in a real interview...",
        key=f"answer_{q_num}"
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        submit_answer = st.button(
            "📤 Submit Answer & Get Feedback",
            use_container_width=True,
            type="primary",
            disabled=not answer.strip()
        )
    with col2:
        skip = st.button("⏭️ Skip Question", use_container_width=True)

    if skip:
        # Record skip with score 0
        st.session_state["interview_session"].append({
            "question": current_q,
            "answer":   "[Skipped]",
            "feedback": "Question was skipped.",
            "score":    0,
            "q_type":   current_qt,
        })
        st.session_state["awaiting_answer"] = False
        st.session_state["current_question"] = None
        st.rerun()

    if submit_answer and answer.strip():
        with st.spinner("🤖 Evaluating your answer..."):
            eval_prompt = get_interview_eval_prompt(role, current_q, answer.strip())
            feedback = query_model(INTERVIEW_EVAL_SYSTEM_PROMPT, eval_prompt)
            score = _extract_score(feedback)

        # Save to session
        st.session_state["interview_session"].append({
            "question": current_q,
            "answer":   answer.strip(),
            "feedback": feedback,
            "score":    score,
            "q_type":   current_qt,
        })
        st.session_state["awaiting_answer"] = False
        st.session_state["current_question"] = None
        st.rerun()


def _render_summary():
    """Render the full performance summary."""
    session = st.session_state["interview_session"]
    role    = st.session_state["interview_role"]

    st.markdown("### 📊 Full Performance Summary")

    scores = [item["score"] for item in session if item["score"] > 0]
    avg    = round(sum(scores) / len(scores), 1) if scores else 0

    # Quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Questions Answered", len(session))
    with col2:
        st.metric("Average Score", f"{avg}/10")
    with col3:
        grade = "Excellent 🌟" if avg >= 8 else "Good 👍" if avg >= 6 else "Needs Work 📚" if avg >= 4 else "Keep Practicing 💪"
        st.metric("Grade", grade)

    st.markdown("---")

    # Generate AI summary
    with st.spinner("🤖 Generating personalized performance report..."):
        summary_prompt = get_interview_summary_prompt(session)
        summary        = query_model(INTERVIEW_SUMMARY_SYSTEM_PROMPT, summary_prompt)

    st.markdown(summary)

    st.markdown("---")

    # Download
    report = f"# Mock Interview Report — {role}\n\n"
    report += f"**Average Score:** {avg}/10\n\n---\n\n"
    for i, item in enumerate(session, 1):
        report += f"## Q{i}: {item['question']}\n\n"
        report += f"**Answer:** {item['answer']}\n\n"
        report += f"**Score:** {item['score']}/10\n\n"
        report += f"**Feedback:**\n{item['feedback']}\n\n---\n\n"
    report += f"## Performance Summary\n\n{summary}"

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📥 Download Full Report (Markdown)",
            data=report,
            file_name=f"interview_report_{role.replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    with col2:
        if st.button("🔄 Start New Interview", use_container_width=True):
            _reset_interview()
            st.rerun()


def _reset_interview():
    """Reset all interview session state."""
    for key in ["interview_session", "current_question", "interview_active",
                "awaiting_answer", "show_summary", "interview_role",
                "interview_q_types", "current_q_type"]:
        st.session_state.pop(key, None)
