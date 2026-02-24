# 🚀 Career Assistant Platform

**Your AI-powered career guidance system for any field**

Get personalized roadmaps, mentorship, project ideas, resume feedback, and interview prep—all in one intelligent system.

> **✨ NEW:** Multi-profile support, data persistence, analytics dashboard, and skill assessments! See [README_ENHANCEMENTS.md](README_ENHANCEMENTS.md) for details.

---

## 📋 Overview

**Career Assistant Platform** is a Streamlit-based intelligent platform designed to guide students, freshers, and professionals who want structured career development in **any field**.

Whether you're transitioning to a new role, starting a new career, or advancing in your current field, this platform provides:
- 🗺️ Personalized career roadmaps
- 💬 AI-powered career mentorship
- 💡 Portfolio-building project ideas
- 📄 Resume analysis and feedback
- 🎤 Mock interview practice

All recommendations are **tailored to your profile** and **specific domain**.

---

## 🎯 Core Features

### 1. **Career Roadmap Generator**
Get a structured, personalized learning path to your goal.

**You provide:**
- Current Skill Level (Beginner / Intermediate / Advanced)
- Target Role / Field
- Daily Time Availability
- Target Timeline (3 / 6 / 12 months)

**System generates:**
- ✅ Monthly milestones with clear deliverables
- ✅ Weekly structured learning plan
- ✅ Required skills (technical & soft)
- ✅ Recommended tools and resources
- ✅ Portfolio and project suggestions
- ✅ Interview preparation timeline

### 2. **Smart Chat Mentor**
Chat with an AI expert specialized in your chosen domain.

**Capabilities:**
- 💬 Domain-specific doubt clarification
- 💬 Career guidance and advice
- 💬 Concept explanation with examples
- 💬 Industry insights and trends
---

## 📖 How to Use

### Step 1: Configure Your Profile
1. Open the app and go to the **⚙️ Configuration** section in the sidebar
2. Enter:
   - **Current Skill Level** - Beginner, Intermediate, or Advanced
   - **Target Role / Field** - What you want to become (e.g., "Data Scientist", "Product Manager")
   - **Daily Time Availability** - How much time you can dedicate daily
   - **Target Timeline** - When you want to achieve this (3, 6, or 12 months)
3. Click **"💾 Save Configuration"**

### Step 2: Use the Modules

#### 🗺️ **Career Roadmap Tab:**
- Click "📋 Generate Roadmap"
- Review monthly milestones, weekly plans, and required skills
- Save your personalized roadmap

#### 💬 **Smart Chat Mentor Tab:**
- Ask any question about your domain
- Chat history is maintained during your session
- Get domain-specific, expert advice

#### 💡 **Project Ideas Tab:**
- Click "💡 Generate Project Ideas"
- Review 3-5 portfolio-building projects
- Choose projects that excite you

#### 📄 **Resume Analyzer Tab:**
- Paste your resume text
- Click "🔍 Analyze Resume"
- Get detailed feedback and improvement suggestions

#### 🎤 **Mock Interview Tab:**
- Click "🎤 Start Interview"
- Answer 5 role-specific interview questions
- Get feedback after each answer
- Review complete interview performance

---

## 🎨 User Interface

### Navigation Structure

```
Career Assistant Platform
├── ⚙️ Configuration (Sidebar)
│   ├── Current Skill Level
│   ├── Target Role/Field
│   ├── Daily Time Availability
│   └── Target Timeline
│
└── Main Content (5 Tabs)
    ├── 🗺️ Career Roadmap
    ├── 💬 Smart Chat Mentor
    ├── 💡 Project Ideas
    ├── 📄 Resume Analyzer
    └── 🎤 Mock Interview
```

### Design Features

- **Dark Theme:** NeuralChat-inspired gradient background
- **Color Scheme:** Cyan, Magenta, Gold accents with high contrast
- **Responsive Layout:** Works on desktop, tablet, and mobile
- **Accessibility:** High contrast text, clear button labels

---

## 📁 Project Structure

```
ai_study/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── utils/
│   ├── __init__.py
│   ├── llm.py                 # LLM query interface (HuggingFace)
│   └── prompts.py             # Prompt generation functions
│
├── assets/
│   └── streamlit_style.css    # Custom CSS styling
│
└── .env                        # Environment variables (create this)
```

---

## 🔧 Configuration & Customization

### Environment Setup

1. **Create `.env` file:**
```env
HF_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxx
```

2. **Get API Key:**
   - Visit https://huggingface.co/settings/tokens
   - Create new token (free tier available)
   - Copy your token to `.env` file

### Customization Options

**Change LLM Model:**
Edit `utils/llm.py` line 18 to use different Llama model

**Adjust Response Length:**
Edit `app.py` - change `max_tokens` in query_model() calls

**Modify Theme Colors:**
Edit `assets/streamlit_style.css`

**Interview Question Limit:**
Edit `app.py` line ~400

---

## 🐛 Troubleshooting

### Issue: "No module named 'huggingface_hub'"
```bash
pip install huggingface_hub
# or
pip install -r requirements.txt
```

### Issue: "HF_API_KEY not found"
1. Create `.env` file in project root
2. Add: `HF_API_KEY=your_key_here`
3. Get free key from HuggingFace Hub

### Issue: Application runs but no responses from AI
1. Check internet connection
2. Verify HuggingFace API key is valid
3. Check HuggingFace API quota
4. Try restarting the app

### Issue: Slow responses
1. Reduce `max_tokens` values
2. Use a lighter LLM model
3. Check internet speed

---

## 🚀 Deployment

### Streamlit Cloud (Free)
```bash
git push your-repo
# Deploy at https://streamlit.io/cloud
```

### Docker
```bash
docker build -t career-assistant .
docker run -p 8501:8501 career-assistant
```

---

## 📈 Future Improvements

- [ ] User authentication and profile saving
- [ ] Advanced analytics dashboard
- [ ] Integration with job boards
- [ ] Certification tracking
- [ ] Video explanations support
- [ ] Peer discussion forum
- [ ] Multi-language support
- [ ] PDF resume upload with parsing
- [ ] Real-time progress stats

---

## 💡 Example Use Cases

### Case 1: Career Transition
Marketing professional → Data Scientist

1. Generate career roadmap (6 months)
2. Ask mentor about Python, SQL, ML fundamentals
3. Build portfolio projects
4. Get resume feedback
5. Practice interviews

### Case 2: Fresh Graduate
Computer Science graduate → Software Engineer

1. Create personalized learning path
2. Build 3-4 practical projects
3. Optimize resume with technical keywords
4. Practice coding interviews
5. Get feedback and iterate

### Case 3: Skill Enhancement
Senior developer → Tech Lead

1. Focus on leadership and architecture skills
2. Discuss system design concepts
3. Build complex projects
4. Practice behavioral interviews
5. Prepare for senior-level expectations

---

## 📞 Support & Contact

- **Issues:** Check the troubleshooting section
- **Questions:** Refer to inline code documentation
- **Feature Requests:** Open an issue in repository

---

## 📜 License

This project is open-source and free to use for educational and professional purposes.

---

## 🙏 Acknowledgments

- **Streamlit:** For the amazing web framework
- **HuggingFace:** For Llama models and inference API
- **Open Source Community:** For tools and libraries

---

## 💡 Tips for Maximum Success

1. **Be Specific:** Detailed profiles = better recommendations
2. **Consistency:** Regular practice over cramming
3. **Build Projects:** Projects > Certifications for most roles
4. **Practice Interviews:** Mock interviews improve performance
5. **Update Resume:** Keep it updated as you progress
6. **Ask Questions:** Use chat mentor generously
7. **Stay Current:** Learn latest trends in your field

---

**Happy Career Development! 🚀**

---

*Career Assistant Platform | Last Updated: February 2026*
*Powered by AI | Built with Streamlit*
- Check your internet connection
- Verify HF_API_KEY is set
- Ensure huggingface_hub is installed

### Issue: App crashes on specific day
- Clear browser cache
- Restart the Streamlit app
- Check error logs in terminal

### Issue: Progress not saving
- Progress is saved in session state
- Session resets on browser refresh
- Consider adding database for persistence

---

## 🚀 Future Enhancements

- [ ] Database-based progress tracking
- [ ] User authentication system
- [ ] Mobile app version
- [ ] Real-time analytics dashboard
- [ ] Peer collaboration features
- [ ] Certificate generation
- [ ] Adaptive learning paths
- [ ] Video tutorials integration

---

## 📄 License

This educational content is provided as-is for learning purposes.

---

## 🙏 Acknowledgments

- Streamlit for the amazing web framework
- HuggingFace for LLM API
- AI community for inspiration

---

**Ready to become job-ready? Start Day 1 now! 🎓**

---

## 📞 Questions?

Use the **AI Mentor** tab in the app to ask any questions about the course.

**Happy Learning! 🚀**
