"""
skills.py — Skill Assessment Module
Evaluate user skills and provide improvement recommendations.
"""

import streamlit as st
from modules.chat import query_model
from prompts.skills_prompt import get_skill_assessment_prompt, get_skill_recommendations_prompt
import json


def render_skills():
    """Render the skill assessment interface."""
    st.markdown("""
    <div class="module-header">
        <div class="module-icon">🎯</div>
        <div>
            <h2>Skill Assessment</h2>
            <p>Evaluate your current skills and identify improvement areas</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if user has a profile
    if "current_profile" not in st.session_state or not st.session_state.current_profile:
        st.warning("⚠️ Please select or create a career profile first!")
        return
    
    profile = st.session_state.current_profile
    career_field = profile.get("career_field", "")
    
    # Create two columns: Assessment Input & Results
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    with col1:
        st.subheader("📝 Self Assessment")
        
        # Skill assessment form
        with st.form("skill_assessment_form"):
            st.info("Rate your proficiency in key skills for your field")
            
            # Technical Skills
            st.markdown("### 💻 Technical Skills")
            tech_skills = {}
            skill_names = [
                "Programming/Coding",
                "Data Analysis",
                "Tools & Frameworks",
                "System Design",
                "Problem Solving"
            ]
            for skill in skill_names:
                tech_skills[skill] = st.slider(
                    f"{skill}",
                    1, 10,
                    value=5,
                    key=f"tech_{skill}"
                )
            
            # Soft Skills
            st.markdown("### 🌟 Soft Skills")
            soft_skills = {}
            soft_skill_names = [
                "Communication",
                "Teamwork",
                "Leadership",
                "Time Management",
                "Adaptability"
            ]
            for skill in soft_skill_names:
                soft_skills[skill] = st.slider(
                    f"{skill}",
                    1, 10,
                    value=5,
                    key=f"soft_{skill}"
                )
            
            # Additional info
            st.markdown("### 📌 Additional Information")
            years_exp = st.number_input("Years of experience:", 0, 50, 0)
            strongest_area = st.text_input("Your strongest area:")
            weakest_area = st.text_input("Area needing most improvement:")
            
            submitted = st.form_submit_button("🚀 Analyze Skills", use_container_width=True)
        
        if submitted:
            # Store assessment data
            st.session_state.skill_assessment = {
                "technical_skills": tech_skills,
                "soft_skills": soft_skills,
                "years_experience": years_exp,
                "strongest": strongest_area,
                "weakest": weakest_area
            }
            
            # Save to profile
            profile["skill_assessment"] = st.session_state.skill_assessment
            st.session_state.profile_manager.update_profile(profile["name"], st.session_state.skill_assessment)
            
            st.success("✅ Assessment saved! Check recommendations →")
    
    with col2:
        st.subheader("📊 Assessment Results")
        
        if "skill_assessment" in st.session_state:
            assessment = st.session_state.skill_assessment
            
            # Display current scores
            st.markdown("#### 📈 Your Scores")
            
            # Technical skills overview
            tech_avg = sum(assessment["technical_skills"].values()) / len(assessment["technical_skills"])
            st.metric("Technical Skills 💻", f"{tech_avg:.1f}/10", 
                     int(tech_avg) - 5 if tech_avg > 5 else int(tech_avg) - 5)
            
            # Soft skills overview
            soft_avg = sum(assessment["soft_skills"].values()) / len(assessment["soft_skills"])
            st.metric("Soft Skills 🌟", f"{soft_avg:.1f}/10",
                     int(soft_avg) - 5 if soft_avg > 5 else int(soft_avg) - 5)
            
            # Overall score
            overall = (tech_avg + soft_avg) / 2
            st.metric("Overall Score", f"{overall:.1f}/10",
                     int(overall) - 5 if overall > 5 else int(overall) - 5)
            
            st.divider()
            
            # Visualize skill breakdown
            st.markdown("#### 🎯 Skill Breakdown")
            
            # Create expandable sections for detailed breakdown
            with st.expander("Technical Skills Details"):
                for skill, score in assessment["technical_skills"].items():
                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        st.progress(score / 10, text=skill)
                    with col_b:
                        st.caption(f"{score}/10")
            
            with st.expander("Soft Skills Details"):
                for skill, score in assessment["soft_skills"].items():
                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        st.progress(score / 10, text=skill)
                    with col_b:
                        st.caption(f"{score}/10")
            
            # AI-powered recommendations
            st.divider()
            st.markdown("#### 🤖 AI Recommendations")
            
            if st.button("Get Personalized Recommendations", use_container_width=True, key="get_recs"):
                with st.spinner("Analyzing your skills..."):
                    try:
                        prompt = get_skill_recommendations_prompt(
                            career_field=career_field,
                            tech_skills=assessment["technical_skills"],
                            soft_skills=assessment["soft_skills"],
                            years_exp=assessment["years_experience"],
                            strongest=assessment["strongest"],
                            weakest=assessment["weakest"]
                        )
                        
                        response = query_model(prompt)
                        st.markdown("### 💡 Improvement Plan")
                        st.markdown(response)
                        
                        # Save recommendations
                        st.session_state.skill_recommendations = response
                        
                    except Exception as e:
                        st.error(f"Error getting recommendations: {str(e)}")
        
        else:
            st.info("💡 Complete the assessment form on the left to see your results and recommendations.")
    
    # Skills Comparison (if multiple assessments exist)
    st.divider()
    st.markdown("### 📊 Track Your Growth")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="tips-box">
            <h4>💪 Strength Building Tips</h4>
            <ul>
                <li>Focus on weak areas first</li>
                <li>Practice consistently (1-2 hours/day)</li>
                <li>Build real projects to demonstrate skills</li>
                <li>Seek mentorship in weak areas</li>
                <li>Regular self-assessment (monthly)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown("""
        <div class="tips-box">
            <h4>🎯 Improvement Strategies</h4>
            <ul>
                <li>Enroll in targeted courses</li>
                <li>Contribute to open-source projects</li>
                <li>Participate in hackathons/competitions</li>
                <li>Read industry blogs & research papers</li>
                <li>Network with experienced professionals</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
