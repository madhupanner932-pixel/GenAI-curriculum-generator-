# Quick Start Guide - Career Assistant Platform v2.0

## 🚀 5-Minute Setup

### Step 1: Install Dependencies (1 minute)
```bash
pip install -r requirements.txt
```

### Step 2: Set Up Environment (30 seconds)
Create a `.env` file in the project root:
```
HUGGINGFACE_API_KEY=your_api_key_here
```

Get your free API key from [HuggingFace Hub](https://huggingface.co/settings/tokens)

### Step 3: Launch the App (30 seconds)
```bash
python -m streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📋 First-Time Workflow (5 minutes)

### 1. Create Your Profile (1 minute)
- Enter your **Career Field** (e.g., "Data Science", "Web Development")
- Write your **Career Goal** (e.g., "Become a Senior Data Scientist")
- Select your **Experience Level** (Beginner/Intermediate/Advanced/Expert)
- Click **"💾 Save Configuration"**

✅ **Result**: Your profile is created and saved locally

### 2. Generate Your Roadmap (2 minutes)
- Go to **🗺️ Roadmap** tab
- Click **"Generate Roadmap"**
- Review the AI-generated career roadmap
- Click **"📥 Save Roadmap to Profile"**

✅ **Result**: Personalized 6-12 month roadmap saved

### 3. Take a Skill Assessment (2 minutes)
- Go to **📝 Assessment** tab
- Select a topic (e.g., "Python Fundamentals")
- Choose number of questions (5-10)
- Click **"Start Assessment"**
- Answer all questions
- Click **"Submit Assessment"**

✅ **Result**: Instant score, skill level, and feedback

### 4. View Your Analytics (Optional)
- Go to **📊 Analytics** tab
- See your engagement score, assessment results
- Download reports in TXT/CSV/JSON formats

✅ **Result**: Complete overview of your progress

---

## 🎯 Feature Overview

| Feature | Tab | Purpose | Time |
|---------|-----|---------|------|
| **Career Roadmap** | 🗺️ | AI-generated career path | 5 min |
| **Chat Mentor** | 💬 | Ask career questions | Ongoing |
| **Project Ideas** | 💡 | Portfolio projects | 5 min |
| **Resume Analysis** | 📄 | Get resume feedback | 5 min |
| **Interview Practice** | 🎤 | Mock interviews with feedback | 10 min |
| **Skill Tests** | 📝 | Assessment 20+ questions | 10 min |
| **Analytics** | 📊 | Track progress & export data | 2 min |

---

## 💻 Common Tasks

### Task 1: Chat with Your Career Mentor
```
1. Open 💬 Chat Mentor tab
2. Type your question: "What skills do I need for a senior role?"
3. Get instant AI-powered advice
4. Chat history is automatically saved to your profile
```

### Task 2: Practice for an Interview
```
1. Open 🎤 Interview tab
2. Select interview type (Behavioral/Technical/Case Study)
3. Enter target role
4. Click "Start Interview Practice"
5. Answer questions and get feedback
6. Click "💾 Save Interview Session"
```

### Task 3: Analyze Your Resume
```
1. Open 📄 Resume tab
2. Paste your resume content
3. Click "Analyze Resume"
4. Get specific feedback and improvement suggestions
5. Automatically saved to your profile
```

### Task 4: Download Your Progress Report
```
1. Open 📊 Analytics tab
2. Choose export format:
   - 📄 TXT: Human-readable report
   - 📊 CSV: Spreadsheet format
   - 📋 JSON: Raw data export
3. Click corresponding button
4. File downloads to your computer
```

### Task 5: Compare Multiple Profiles
```
1. Create multiple profiles (different career paths)
2. Open Analytics for each
3. Download CSV/JSON for all profiles
4. Compare progress across different goals
```

---

## 📂 Where Your Data Is Stored

All data is saved **locally** in the `data/` folder:

```
data/
├── profiles/          # Your profile configurations
├── results/           # Roadmaps, resume analysis, interview recordings
└── backups/           # Automatic backups of your data
```

**Privacy**: No data leaves your computer. Everything stays local.

---

## 🔧 Troubleshooting

### Issue: "No module named 'streamlit'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "HUGGINGFACE_API_KEY not found"
**Solution:**
1. Create `.env` file in project root
2. Add: `HUGGINGFACE_API_KEY=your_key`
3. Restart the app

### Issue: "Profile not saving"
**Solution:**
- Ensure both fields are filled
- Check you have write permissions to project folder
- Try a simpler profile name (no special characters)

### Issue: "Port 8501 already in use"
**Solution:**
```bash
python -m streamlit run app.py --server.port 8502
```

### Issue: "LLM not responding"
**Solution:**
- Check internet connection
- Verify API key is correct
- Check HuggingFace API status
- Wait a few seconds and retry

---

## 🎓 Recommended Workflow

### Week 1: Foundation
- ✅ Create profile
- ✅ Generate career roadmap
- ✅ Take assessment in main skill area
- ✅ Chat with mentor about weak areas

### Week 2-4: Build Skills
- ✅ Take remaining assessments
- ✅ Practice interviews 2-3 times
- ✅ Chat about specific topics each week
- ✅ Generate project ideas and start one

### Week 5-8: Advanced
- ✅ Analyze resume and refine
- ✅ Practice behavioral interviews
- ✅ Complete all assessments
- ✅ Download progress report

### Ongoing
- ✅ Monthly check-ins in Chat Mentor
- ✅ Quarterly assessment refreshers
- ✅ Track progress in Analytics

---

## 📊 Understanding Your Metrics

### Engagement Score (0-100)
- **0-25**: Just getting started
- **26-50**: Actively learning
- **51-75**: Highly engaged
- **76-100**: Fully committed

**How it's calculated:**
- Chat messages: 0.4 × count
- Roadmaps completed: +10 each
- Resumes analyzed: +15 each
- Interview sessions: +20 each

### Assessment Levels
- ⭐: Beginner (0-59%)
- ⭐⭐: Intermediate (60-69%)
- ⭐⭐⭐: Proficient (70-79%)
- ⭐⭐⭐⭐: Advanced (80-89%)
- ⭐⭐⭐⭐⭐: Expert (90%+)

---

## 🔐 Data Security

### What's Kept Local
- ✅ All profile information
- ✅ Chat history
- ✅ Assessment scores
- ✅ Resume analysis
- ✅ Generated roadmaps
- ✅ Interview practice records

### What's NOT Stored Anywhere
- ❌ Your API key (only in local `.env`)
- ❌ Your searches history
- ❌ Session cookies
- ❌ Tracking data

### Backup Your Data
```bash
# Automatic backups in data/backups/
# Manual export from Analytics tab
# Download as JSON for safekeeping
```

---

## 📞 Getting Help

### Check These Resources
1. [README_ENHANCEMENTS.md](README_ENHANCEMENTS.md) - Full feature documentation
2. [FEATURE_REFERENCE.md](FEATURE_REFERENCE.md) - API and technical reference
3. Console output - When errors occur

### Common Questions

**Q: Can I export my data?**  
A: Yes! Analytics tab has TXT, CSV, and JSON export options.

**Q: Is my resume kept private?**  
A: Yes! All data is stored locally. Nothing is uploaded to external servers.

**Q: Can I have multiple careers?**  
A: Absolutely! Create separate profiles for each career path.

**Q: How often should I take assessments?**  
A: Every 2-4 weeks to track improvement. Try different topics to find strengths/weaknesses.

**Q: Does chat history reset?**  
A: No! All chat history is saved to your profile and persists between sessions.

---

## 🎯 Success Tips

1. **Be Specific**: Write clear career goals for better AI recommendations
2. **Regular Practice**: Interview practice and assessments 1-2x per week
3. **Track Progress**: Download monthly reports to see improvement
4. **Iterate**: Update your profile as your goals evolve
5. **Explore**: Try all features - each provides different insights

---

## 📈 Next Steps

After completing the quick start:

1. **Explore Advanced Assessment Topics**
   - Complete all 4 assessment topics
   - Compare your scores across areas
   - Focus on weakest areas

2. **Practice Multiple Interview Styles**
   - Try Behavioral, Technical, Case Study
   - Practice same role multiple times
   - See how your answers improve

3. **Build Your Portfolio**
   - Use Project Ideas from 💡 Projects tab
   - Ask mentor for guidance on each project
   - Document your projects in resume

4. **Refine Your Resume**
   - Paste current resume in 📄 Resume tab
   - Get detailed feedback
   - Update and re-analyze monthly

5. **Track Long-Term Progress**
   - Download monthly progress reports
   - Monitor engagement score growth
   - Celebrate assessment score improvements

---

## 🚀 Ready to Get Started?

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure
# Create .env with your API key

# 3. Launch
python -m streamlit run app.py

# 4. Create your first profile and start learning!
```

**Let's build your career! 💪**

---

**Version**: 2.0  
**Last Updated**: February 24, 2026  
**Setup Time**: ~5 minutes  
**Estimated Learning Time**: Flexible
