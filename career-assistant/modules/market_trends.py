"""
market_trends.py — Real-Time Market Trend Intelligence
Trending skills, salary data, hiring demand index.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# Market data (can be replaced with real APIs later)
MARKET_DATA = {
    "trending_skills": {
        "AWS": {"trend": 18, "demand": "Very High", "salary_min": 120000, "salary_max": 180000},
        "Kubernetes": {"trend": 22, "demand": "Very High", "salary_min": 130000, "salary_max": 200000},
        "Python": {"trend": 5, "demand": "Very High", "salary_min": 100000, "salary_max": 160000},
        "Machine Learning": {"trend": 25, "demand": "Very High", "salary_min": 140000, "salary_max": 220000},
        "DevOps": {"trend": 15, "demand": "High", "salary_min": 125000, "salary_max": 190000},
        "React": {"trend": 3, "demand": "High", "salary_min": 110000, "salary_max": 170000},
        "Go/Golang": {"trend": 28, "demand": "High", "salary_min": 115000, "salary_max": 180000},
        "Cloud Architecture": {"trend": 32, "demand": "Very High", "salary_min": 140000, "salary_max": 210000},
        "Data Science": {"trend": 12, "demand": "High", "salary_min": 130000, "salary_max": 200000},
        "Terraform": {"trend": 35, "demand": "High", "salary_min": 120000, "salary_max": 190000},
    },
    "location_salaries": {
        "India": {"min": 18, "max": 50, "currency": "LPA", "growth": 12},
        "US": {"min": 120, "max": 250, "currency": "K USD", "growth": 5},
        "UK": {"min": 80, "max": 160, "currency": "K GBP", "growth": 4},
        "Canada": {"min": 100, "max": 200, "currency": "K CAD", "growth": 8},
    },
    "demand_index": {
        "DevOps": 95,
        "Cloud Architecture": 98,
        "ML Engineer": 92,
        "Full Stack": 88,
        "Data Science": 91,
        "Security": 90,
    }
}


def get_trending_skills_data():
    """Get trending skills with visualizations."""
    skills = list(MARKET_DATA["trending_skills"].keys())
    trends = [MARKET_DATA["trending_skills"][s]["trend"] for s in skills]
    
    df = pd.DataFrame({
        "Skill": skills,
        "Growth %": trends,
        "Avg Salary": [
            (MARKET_DATA["trending_skills"][s]["salary_min"] + 
             MARKET_DATA["trending_skills"][s]["salary_max"]) / 2 
            for s in skills
        ],
    }).sort_values("Growth %", ascending=False)
    
    return df


def get_salary_comparison(location="India", skill="AWS"):
    """Get salary data for location and skill."""
    if location not in MARKET_DATA["location_salaries"]:
        location = "India"
    
    salary_data = MARKET_DATA["location_salaries"][location]
    
    if skill in MARKET_DATA["trending_skills"]:
        skill_data = MARKET_DATA["trending_skills"][skill]
        # Adjust salary by location multiplier
        if location == "India":
            min_sal = skill_data["salary_min"] / 8  # Convert to LPA
            max_sal = skill_data["salary_max"] / 8
        elif location == "US":
            min_sal = skill_data["salary_min"]
            max_sal = skill_data["salary_max"]
        else:
            min_sal = skill_data["salary_min"] * 0.8
            max_sal = skill_data["salary_max"] * 0.8
    else:
        min_sal = salary_data["min"]
        max_sal = salary_data["max"]
    
    return {
        "min": min_sal,
        "max": max_sal,
        "currency": salary_data["currency"],
        "growth": salary_data["growth"],
    }


def render_market_trends():
    """Render market trend intelligence."""
    st.markdown("""
    <div class="module-header">
        <div class="module-icon">📊</div>
        <div>
            <h2>Real-Time Market Trend Intelligence</h2>
            <p>Trending skills, salary data, and hiring demand across markets</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔥 Trending Skills", "💰 Salary Trends", "📈 Demand Index", "🌍 Location Insights"])
    
    with tab1:
        st.subheader("🔥 Top Trending Skills (YoY Growth)")
        
        df = get_trending_skills_data()
        
        # Bar chart
        fig = px.bar(
            df,
            x="Skill",
            y="Growth %",
            color="Growth %",
            color_continuous_scale="RdYlGn",
            title="Skill Demand Growth Rate (%)",
            labels={"Growth %": "YoY Growth %"},
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Detailed skill table
        st.markdown("### 📋 Detailed Skill Analysis")
        
        trending_df = pd.DataFrame([
            {
                "Skill": skill,
                "Growth": f"+{MARKET_DATA['trending_skills'][skill]['trend']}%",
                "Demand": MARKET_DATA["trending_skills"][skill]["demand"],
                "Avg Salary": f"${(MARKET_DATA['trending_skills'][skill]['salary_min'] + MARKET_DATA['trending_skills'][skill]['salary_max']) // 2 / 1000:.0f}K",
            }
            for skill in MARKET_DATA["trending_skills"].keys()
        ])
        
        st.dataframe(
            trending_df.sort_values("Growth", ascending=False, 
                                   key=lambda x: x.str.replace("%", "").astype(int) if x.dtype == "object" else x),
            use_container_width=True,
            hide_index=True
        )
    
    with tab2:
        st.subheader("💰 Salary Trends by Skill & Location")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_skill = st.selectbox(
                "Select skill",
                list(MARKET_DATA["trending_skills"].keys()),
                key="salary_skill"
            )
        
        with col2:
            selected_location = st.selectbox(
                "Select location",
                list(MARKET_DATA["location_salaries"].keys()),
                key="salary_location"
            )
        
        # Get salary data
        salary_info = get_salary_comparison(selected_location, selected_skill)
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Min Salary",
                f"{salary_info['min']:.0f} {salary_info['currency']}"
            )
        
        with col2:
            avg = (salary_info['min'] + salary_info['max']) / 2
            st.metric(
                "Avg Salary",
                f"{avg:.0f} {salary_info['currency']}"
            )
        
        with col3:
            st.metric(
                "Market Growth",
                f"+{salary_info['growth']}%",
                "YoY"
            )
        
        st.divider()
        
        # Salary range visualization
        salary_range_df = pd.DataFrame({
            "Category": ["Min", "Average", "Max"],
            "Salary": [
                salary_info['min'],
                (salary_info['min'] + salary_info['max']) / 2,
                salary_info['max'],
            ]
        })
        
        fig = go.Figure(data=[
            go.Bar(
                x=salary_range_df["Category"],
                y=salary_range_df["Salary"],
                marker_color=["#FF6584", "#6C63FF", "#43E97B"],
                text=[f"{s:.0f} {salary_info['currency']}" for s in salary_range_df["Salary"]],
                textposition="auto",
            )
        ])
        fig.update_layout(
            title=f"{selected_skill} Salary Range in {selected_location}",
            yaxis_title="Salary",
            height=400,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("📈 Hiring Demand Index")
        
        demand_df = pd.DataFrame([
            {"Role": role, "Demand Score": score}
            for role, score in MARKET_DATA["demand_index"].items()
        ]).sort_values("Demand Score", ascending=False)
        
        # Gauge chart
        fig = go.Figure(data=[
            go.Bar(
                y=demand_df["Role"],
                x=demand_df["Demand Score"],
                orientation="h",
                marker=dict(
                    color=demand_df["Demand Score"],
                    colorscale="RdYlGn",
                    showscale=True,
                    cmin=0,
                    cmax=100,
                ),
                text=[f"{score}/100" for score in demand_df["Demand Score"]],
                textposition="auto",
            )
        ])
        fig.update_layout(
            title="Current Hiring Demand by Role",
            xaxis_title="Demand Score (Out of 100)",
            yaxis_title="Role",
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Interpretation
        st.markdown("### 📊 What This Means")
        
        for role, score in MARKET_DATA["demand_index"].items():
            if score >= 95:
                emoji = "🟢"
                text = "Critical demand - Great time to learn"
            elif score >= 85:
                emoji = "🟡"
                text = "High demand - Good career path"
            else:
                emoji = "🟠"
                text = "Moderate demand - Still viable"
            
            st.write(f"{emoji} **{role}** ({score}/100): {text}")
    
    with tab4:
        st.subheader("🌍 Location Market Analysis")
        
        locations = list(MARKET_DATA["location_salaries"].keys())
        
        location_analysis = pd.DataFrame([
            {
                "Location": loc,
                "Min Salary": MARKET_DATA["location_salaries"][loc]["min"],
                "Max Salary": MARKET_DATA["location_salaries"][loc]["max"],
                "Growth": f"+{MARKET_DATA['location_salaries'][loc]['growth']}%",
                "Hiring Growth": MARKET_DATA["location_salaries"][loc]["growth"],
            }
            for loc in locations
        ])
        
        # Growth comparison
        fig = px.bar(
            location_analysis,
            x="Location",
            y="Hiring Growth",
            color="Hiring Growth",
            color_continuous_scale="Blues",
            title="Market Growth by Location (YoY %)",
            labels={"Hiring Growth": "Growth %"},
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        st.markdown("### 💡 Location Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🟢 Best for Growth:** US & Canada")
            st.caption("Higher salaries, strong market demand")
        
        with col2:
            st.markdown("**🟡 Best for Value:** India")
            st.caption("Growing market, tech hub, lower cost of living")
        
        st.divider()
        
        st.markdown("### 📋 Salary Comparison Table")
        st.dataframe(
            location_analysis[["Location", "Min Salary", "Max Salary", "Growth"]],
            use_container_width=True,
            hide_index=True,
        )
        
        # Pro tip
        st.info(
            """
            **💡 Pro Tips:**
            - Remote work changing location advantage - skills now valued globally
            - US market highest salaries, India fastest growth
            - Timezone flexibility increases opportunities
            """
        )
