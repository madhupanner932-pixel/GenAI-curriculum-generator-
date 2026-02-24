"""
resume_gap_analyzer.py — Advanced Resume Skill Gap Analyzer
Upload resume, extract skills, compare with jobs, show readiness score.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
from modules.resume import extract_text_from_pdf, extract_text_from_docx
import re


# Job descriptions database by role
JOB_REQUIREMENTS = {
    "Cloud Architect": {
        "AWS": 9,
        "Kubernetes": 8,
        "Terraform": 8,
        "System Design": 9,
        "Security": 8,
        "Cost Optimization": 7,
        "Networking": 8,
        "Database Design": 7,
        "DevOps": 8,
        "Leadership": 7,
    },
    "Data Scientist": {
        "Python": 9,
        "Machine Learning": 9,
        "Statistics": 9,
        "SQL": 8,
        "Data Visualization": 8,
        "Deep Learning": 7,
        "PyTorch/Tensorflow": 8,
        "Big Data": 7,
        "Data Engineering": 7,
        "Communication": 8,
    },
    "DevOps Engineer": {
        "Docker": 9,
        "Kubernetes": 9,
        "CI/CD": 9,
        "Linux": 9,
        "AWS": 8,
        "Infrastructure as Code": 9,
        "Monitoring": 8,
        "Scripting": 8,
        "Networking": 7,
        "Security": 8,
    },
    "Full Stack Developer": {
        "React": 8,
        "Node.js": 8,
        "JavaScript": 9,
        "Databases": 8,
        "APIs": 8,
        "HTML/CSS": 8,
        "Git": 7,
        "Testing": 7,
        "Problem Solving": 9,
        "Communication": 7,
    },
    "Machine Learning Engineer": {
        "Python": 9,
        "Machine Learning": 9,
        "Deep Learning": 8,
        "Statistics": 9,
        "PyTorch": 8,
        "TensorFlow": 8,
        "Data Preprocessing": 8,
        "Model Deployment": 7,
        "Big Data": 7,
        "Mathematics": 9,
    },
}

# Skill level estimation keywords
SKILL_KEYWORDS = {
    "Python": ["python", "py"],
    "JavaScript": ["javascript", "js", "react", "node"],
    "AWS": ["aws", "amazon web services", "ec2", "s3", "lambda"],
    "Kubernetes": ["kubernetes", "k8s", "docker", "container"],
    "SQL": ["sql", "database", "postgres", "mysql"],
    "Machine Learning": ["machine learning", "ml", "scikit", "sklearn"],
    "DevOps": ["devops", "ci/cd", "jenkins", "gitlab"],
    "React": ["react", "jsx"],
    "Docker": ["docker", "container"],
    "Git": ["git", "github", "gitlab"],
    "Leadership": ["leadership", "team lead", "manager"],
    "Communication": ["communication", "presentation", "documentation"],
    "Statistics": ["statistics", "statistical"],
    "Deep Learning": ["deep learning", "neural network", "cnn", "rnn"],
    "Terraform": ["terraform", "iac"],
    "Linux": ["linux", "unix", "bash"],
}


def extract_skills_from_resume(resume_text):
    """Extract skills mentioned in resume."""
    extracted_skills = {}
    resume_lower = resume_text.lower()
    
    for skill, keywords in SKILL_KEYWORDS.items():
        for keyword in keywords:
            if keyword in resume_lower:
                extracted_skills[skill] = extracted_skills.get(skill, 0) + 1
    
    return extracted_skills


def calculate_readiness_score(extracted_skills, job_requirements):
    """Calculate % readiness for a role."""
    if not job_requirements:
        return 0
    
    matched_skills = 0
    total_skills = len(job_requirements)
    skill_scores = {}
    
    for skill, required_level in job_requirements.items():
        if skill in extracted_skills:
            # Assume extracted = level 6/10
            score = min(6, required_level)
            skill_scores[skill] = score
            matched_skills += 1
        else:
            skill_scores[skill] = 0
    
    readiness = (matched_skills / total_skills) * 100 if total_skills > 0 else 0
    return readiness, skill_scores


def render_resume_gap_analyzer():
    """Render advanced resume gap analyzer."""
    st.markdown("""
    <div class="module-header">
        <div class="module-icon">📋</div>
        <div>
            <h2>Advanced Resume Skill Gap Analyzer</h2>
            <p>Upload resume → Extract skills → Compare with job requirements → Get readiness score</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Extract", "🎯 Gap Analysis", "🔥 Readiness Score"])
    
    with tab1:
        st.subheader("Step 1: Upload Your Resume")
        
        col1, col2 = st.columns(2)
        
        with col1:
            uploaded_file = st.file_uploader(
                "Upload resume (PDF, DOCX, TXT)",
                type=["pdf", "docx", "txt"]
            )
            
            if uploaded_file:
                file_type = uploaded_file.type
                
                # Extract text based on file type
                if file_type == "application/pdf":
                    resume_text = extract_text_from_pdf(uploaded_file)
                elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    resume_text = extract_text_from_docx(uploaded_file)
                else:
                    resume_text = uploaded_file.read().decode("utf-8")
                
                st.success("✅ Resume uploaded and processed!")
                st.session_state.resume_text = resume_text
        
        with col2:
            # Target role selector
            target_role = st.selectbox(
                "Select target role to compare",
                list(JOB_REQUIREMENTS.keys()),
                key="target_role_analyzer"
            )
            st.session_state.target_role_analyzer = target_role
        
        # Display extracted text preview
        if st.session_state.get("resume_text"):
            with st.expander("📃 Resume Text Preview"):
                st.text_area(
                    "Extracted resume text:",
                    value=st.session_state.resume_text[:1000] + "...",
                    height=150,
                    disabled=True
                )
    
    with tab2:
        st.subheader("Step 2: Skill Gap Analysis")
        
        if not st.session_state.get("resume_text"):
            st.info("📌 Upload a resume first!")
            return
        
        # Extract skills from resume
        extracted_skills = extract_skills_from_resume(st.session_state.resume_text)
        job_reqs = JOB_REQUIREMENTS.get(st.session_state.target_role_analyzer, {})
        
        if not extracted_skills:
            st.warning("⚠️ No recognized skills found in resume. Add more keywords.")
            return
        
        # Calculate scores
        readiness, skill_scores = calculate_readiness_score(extracted_skills, job_reqs)
        
        # Store in session for tab3
        st.session_state.readiness_score = readiness
        st.session_state.skill_scores = skill_scores
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Extracted Skills")
            skills_df = pd.DataFrame(
                list(extracted_skills.items()),
                columns=["Skill", "Mentions"]
            ).sort_values("Mentions", ascending=False)
            st.dataframe(skills_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("### 🎯 Required Skills")
            req_df = pd.DataFrame(
                list(job_reqs.items()),
                columns=["Skill", "Required Level"]
            ).sort_values("Required Level", ascending=False)
            st.dataframe(req_df, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Heatmap visualization
        st.markdown("### 🔥 Skill Gap Heatmap")
        
        heatmap_data = []
        skills_list = list(job_reqs.keys())
        
        for skill in skills_list:
            required = job_reqs[skill]
            current = skill_scores.get(skill, 0)
            gap = required - current
            heatmap_data.append({
                "Skill": skill,
                "Current": current,
                "Required": required,
                "Gap": gap,
            })
        
        heatmap_df = pd.DataFrame(heatmap_data)
        
        # Create heatmap
        gap_values = [row["Gap"] for row in heatmap_data]
        colors = ["red" if g > 0 else "green" for g in gap_values]
        
        fig = go.Figure(data=[
            go.Bar(
                y=[row["Skill"] for row in heatmap_data],
                x=[row["Gap"] for row in heatmap_data],
                orientation="h",
                marker=dict(color=gap_values, colorscale="RdYlGn_r", showscale=True),
                text=[f"+{g:.1f}" for g in gap_values],
                textposition="auto",
            )
        ])
        fig.update_layout(
            title=f"Skill Gaps for {st.session_state.target_role_analyzer}",
            xaxis_title="Skill Gap (Points)",
            yaxis_title="Skill",
            height=500,
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Critical missing skills
        st.markdown("### 🚨 Critical Gaps (Top Priority)")
        critical = [row for row in heatmap_data if row["Gap"] >= 3]
        
        if critical:
            for item in sorted(critical, key=lambda x: x["Gap"], reverse=True)[:5]:
                col_a, col_b, col_c = st.columns([2, 1, 1])
                with col_a:
                    st.write(f"**{item['Skill']}**")
                with col_b:
                    st.metric("Gap", f"+{item['Gap']:.1f}/10", label_visibility="collapsed")
                with col_c:
                    hours = item["Gap"] * 40  # 40 hours per level
                    st.caption(f"~{hours:.0f}h to learn")
        else:
            st.success("✅ No critical gaps! You're well-matched.")
    
    with tab3:
        st.subheader("Step 3: Overall Readiness Score")
        
        if not st.session_state.get("readiness_score"):
            st.info("📌 Complete gap analysis first!")
            return
        
        readiness = st.session_state.readiness_score
        role = st.session_state.target_role_analyzer
        
        # Big readiness display
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #6C63FF 0%, #FF6584 100%); border-radius: 15px; color: white;">
                <h1 style="font-size: 3rem; margin: 0;">{readiness:.0f}%</h1>
                <h3 style="margin: 0.5rem 0; font-size: 1.3rem;">Ready for {role}</h3>
                <p style="margin: 0; opacity: 0.9;">Based on resume analysis</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Readiness breakdown
        st.markdown("### 📈 ReadinessBreakdown")
        
        readiness_levels = {
            0: ("🔴 Not Ready", "Start learning fundamentals"),
            30: ("🟠 Early Stage", "Good foundation, significant gaps"),
            60: ("🟡 Intermediate", "Solid skills, few gaps"),
            80: ("🟢 Well Prepared", "Ready with minor polishing"),
            95: ("🟢🟢 Expert Ready", "Highly qualified for this role"),
        }
        
        match_level = max([k for k in readiness_levels.keys() if readiness >= k])
        label, description = readiness_levels[match_level]
        
        st.markdown(f"**{label}**  \n{description}")
        
        # Learning plan
        st.divider()
        st.markdown("### 📚 Recommended Learning Path")
        
        skill_scores = st.session_state.skill_scores
        gaps = sorted(
            [(s, skill_scores[s]) for s in skill_scores],
            key=lambda x: x[1]
        )
        
        for rank, (skill, score) in enumerate([g for g in gaps if g[1] < 8][:5], 1):
            st.write(f"{rank}. **{skill}** (Current: {score}/10)")
            hours_needed = (8 - score) * 40
            st.caption(f"Estimated: {hours_needed:.0f} hours of practice")
        
        # Export report
        st.divider()
        if st.button("📥 Download Readiness Report"):
            report = f"""
# Resume Skill Gap Analysis Report

**Target Role:** {role}
**Readiness Score:** {readiness:.1f}%
**Analysis Date:** {datetime.now().strftime('%Y-%m-%d')}

## Summary
{label} - {description}

## Skill Breakdown
"""
            for skill, score in sorted(skill_scores.items(), key=lambda x: x[1]):
                report += f"\n- {skill}: {score}/10"
            
            st.download_button(
                "📄 Download as Text",
                report,
                f"readiness_{role.replace(' ', '_')}.txt",
                "text/plain"
            )
