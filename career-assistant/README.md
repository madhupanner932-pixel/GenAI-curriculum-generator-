# 🚀 Career Assistant — AI-Powered Career Guidance Platform

A full-featured, Streamlit-based intelligent career guidance system with 5 core modules.

---

## ✨ Modules

| Module | Description |
|--------|-------------|
| 🗺️ Career Roadmap | Personalized roadmap with milestones, skills, resources & projects |
| 💬 Smart Chat | AI career mentor scoped to your chosen domain |
| 💡 Project Ideas | 5 portfolio-worthy project ideas with tools, datasets & outcomes |
| 📄 Resume Analyzer | Skill gap analysis, ATS keywords, readiness score & suggestions |
| 🎤 Mock Interview | Role-specific questions, answer evaluation & performance summary |

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **AI:** Groq (LLaMA 3) / OpenAI (GPT-4o Mini) / HuggingFace (Mistral)
- **Architecture:** Single `query_model()` + separate prompts per module

---

## ⚡ Quick Start

### 1. Clone / Navigate to the project
```bash
cd career-assistant
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Copy `.env.example` to `.env` and add your key:

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # Mac/Linux
```

Edit `.env`:
```
LLM_PROVIDER=groq
GROQ_API_KEY=your_actual_key_here
```

> 🆓 **Groq is FREE** — Get your key at [console.groq.com](https://console.groq.com)

### 5. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
career-assistant/
├── app.py                  ← Main Streamlit entry point (UI + routing)
├── config.py               ← Provider & model configuration
├── requirements.txt
├── .env.example            ← Copy to .env and add your keys
│
├── modules/                ← One module file per feature
│   ├── roadmap.py
│   ├── chat.py
│   ├── projects.py
│   ├── resume.py
│   └── interview.py
│
├── prompts/                ← Structured system prompts per module
│   ├── roadmap_prompt.py
│   ├── chat_prompt.py
│   ├── projects_prompt.py
│   ├── resume_prompt.py
│   └── interview_prompt.py
│
└── utils/
    └── model.py            ← Single query_model() function
```

---

## 🔑 Supported LLM Providers

| Provider | Free Tier | Speed | Quality | Setup |
|----------|-----------|-------|---------|-------|
| **Groq** ⭐ | ✅ Yes | ⚡ Ultra-fast | Excellent | [console.groq.com](https://console.groq.com) |
| OpenAI | ❌ Paid | Fast | Best | [platform.openai.com](https://platform.openai.com) |
| HuggingFace | ✅ Yes | Slower | Good | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |

Switch providers by changing `LLM_PROVIDER` in your `.env` file.

---

## 📦 Dependencies

```
streamlit>=1.32.0
openai>=1.0.0        (works for Groq too — same API format)
requests>=2.31.0     (for HuggingFace)
python-dotenv>=1.0.0
```

---

## 🗺️ Future Improvements

- [ ] User authentication & saved sessions
- [ ] PDF resume upload & parsing
- [ ] Progress tracking dashboard
- [ ] Roadmap saving feature
- [ ] Interview scoring analytics charts
- [ ] Cloud deployment (Streamlit Cloud / Heroku)
