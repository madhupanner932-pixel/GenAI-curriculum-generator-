"""
skills_prompt.py — Skill Assessment Prompts
"""

def get_skill_assessment_prompt(career_field, tech_skills, soft_skills, years_exp, strongest, weakest):
    """Generate prompt for skill gap analysis."""
    return f"""
You are an expert career coach and skill assessment specialist.

A professional in the field of "{career_field}" has completed a skill self-assessment:

TECHNICAL SKILLS (1-10 scale):
{chr(10).join([f"- {skill}: {score}/10" for skill, score in tech_skills.items()])}

SOFT SKILLS (1-10 scale):
{chr(10).join([f"- {skill}: {score}/10" for skill, score in soft_skills.items()])}

Experience Level: {years_exp} years
Strongest Area: {strongest}
Weakest Area: {weakest}

Please provide:
1. **Skill Gap Analysis** - Identify the most critical gaps for their level
2. **Strengths Leveraging** - How to use their strongest area to improve others
3. **Growth Priorities** - Top 3 skills to focus on in the next 3 months
4. **Learning Pathways** - Specific resources and timelines to improve weak areas
5. **Success Metrics** - How to measure improvement

Format as clear, actionable recommendations.
"""

def get_skill_recommendations_prompt(career_field, tech_skills, soft_skills, years_exp, strongest, weakest):
    """Generate prompt for personalized skill improvement recommendations."""
    tech_avg = sum(tech_skills.values()) / len(tech_skills)
    soft_avg = sum(soft_skills.values()) / len(soft_skills)
    
    return f"""
You are an experienced career development coach specializing in {career_field}.

A professional has completed a comprehensive skill assessment:

PROFILE:
- Field: {career_field}
- Experience: {years_exp} years
- Strongest Area: {strongest}
- Area for Improvement: {weakest}

SKILL SCORES:
Technical Skills Average: {tech_avg:.1f}/10
- {chr(10).join([f"  {skill}: {score}/10" for skill, score in tech_skills.items()])}

Soft Skills Average: {soft_avg:.1f}/10
- {chr(10).join([f"  {skill}: {score}/10" for skill, score in soft_skills.items()])}

Create a PERSONALIZED IMPROVEMENT PLAN that includes:

1. **Executive Summary** - Overall assessment in 2-3 sentences

2. **Skill Gap Analysis** - Most critical areas vs industry expectations

3. **Top 3 Priority Skills**
   For each:
   - Current level vs required level
   - Why this matters for {career_field}
   - Specific action steps (with timelines)

4. **Learning Resources**
   - Online courses/certifications
   - Books and documentation
   - Practice projects
   - Communities to join

5. **2-Month Improvement Plan**
   - Week 1-2: Focus areas
   - Week 3-4: Focus areas
   - Week 5-8: Consolidation and projects

6. **Success Metrics**
   - How to measure progress
   - Realistic improvement targets

Make it concrete, actionable, and motivating!
"""

def get_progress_tracking_prompt(career_field, milestones, completed, in_progress):
    """Generate prompt for progress tracking and motivation."""
    return f"""
You are a supportive career coach for a professional in {career_field}.

ROADMAP PROGRESS:
Total Milestones: {len(milestones)}
Completed: {len(completed)}
In Progress: {len(in_progress)}

Completed Milestones:
{chr(10).join([f"✅ {m}" for m in completed[:5]])} {"..." if len(completed) > 5 else ""}

Current Work:
{chr(10).join([f"⏳ {m}" for m in in_progress[:3]])} {"..." if len(in_progress) > 3 else ""}

Upcoming:
{chr(10).join([f"📌 {m}" for m in milestones[len(completed) + len(in_progress):len(completed) + len(in_progress) + 3]])}

Please provide:
1. **Progress Celebration** - Acknowledge achievements positively
2. **Current Focus** - What to prioritize right now
3. **Momentum Tips** - How to maintain consistency
4. **Potential Obstacles** - Common challenges at this stage
5. **Next Milestone Preparation** - How to prepare for upcoming goals

Keep tone motivational and specific to their situation.
"""
