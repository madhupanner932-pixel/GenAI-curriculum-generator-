"""
modules/chat.py

Smart Chat / Career Mentor module — Streamlit UI + logic.
"""

import streamlit as st
from utils.model import query_model
from prompts.chat_prompt import get_chat_system_prompt
from utils.translations import get_text


def render_chat():
    """Render the Smart Chat / Career Mentor page."""
    
    lang = st.session_state.get("language", "en")

    # ── Header ──────────────────────────────────────────────────────────────
    header_title = "Smart Chat — Career Mentor" if lang == "en" else "ஸ்மார்ட் சாட் — தொழில் மெண்டர்"
    header_desc = "Ask anything about your career journey. Get expert guidance, explanations & strategies." if lang == "en" else "உங்கள் தொழில் பயணத்தைப் பற்றி எதையும் கேளுங்கள். நிபுணத்வ வழிகாட்டல், விளக்கங்கள் மற்றும் உத்திகளைப் பெறுங்கள்."
    
    st.markdown(f"""
    <div class="module-header">
        <span class="module-icon">💬</span>
        <div>
            <h2>{header_title}</h2>
            <p>{header_desc}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Domain Selector ───────────────────────────────────────────────────────
    col1, col2 = st.columns([3, 1])
    with col1:
        domain_label = "🎯 Set your career domain (scope the mentor to your field):" if lang == "en" else "🎯 உங்கள் தொழில் डoමेन் அமைக்கவும்:"
        domain_placeholder = "e.g. Data Science, Web Development, Digital Marketing..." if lang == "en" else "உ.கா: தரவு அறிவியல், வலை மேம்பாடு, டிஜிटல் சந்தைப்படுத்தல்..."
        
        career_domain = st.text_input(
            domain_label,
            value=st.session_state.get("chat_domain", ""),
            placeholder=domain_placeholder,
            key="chat_domain_input"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        clear_label = "🗑️ Clear Chat" if lang == "en" else "🗑️ சாட்டை அழிக்கவும்"
        if st.button(clear_label, use_container_width=True):
            st.session_state["chat_messages"] = []
            st.rerun()

    if career_domain.strip():
        st.session_state["chat_domain"] = career_domain.strip()
    else:
        default_domain = "General Career Development" if lang == "en" else "பொது தொழில் மேம்பாடு"
        career_domain = st.session_state.get("chat_domain", default_domain)

    scope_text = "🔍 Active scope:" if lang == "en" else "🔍 செயல்பாட்டு வரம்பு:"
    st.caption(f"{scope_text} **{career_domain or ('General Career Development' if lang == 'en' else 'பொது தொழில் மேம்பாடு')}**")
    st.markdown("---")

    # ── Initialize chat history ───────────────────────────────────────────────
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = []

    # ── Display existing messages ─────────────────────────────────────────────
    chat_container = st.container()
    with chat_container:
        if not st.session_state["chat_messages"]:
            ready_msg = "Your Career Mentor is ready!" if lang == "en" else "உங்கள் தொழில் மெண்டர் தயாரா!"
            desc_msg = "Ask me about career paths, skills to learn, job hunting tips, industry trends, or anything in your career journey." if lang == "en" else "தொழில் பாதைகள், கற்கிறது திறன்கள், வேலை வேட்டை குறிப்புகள், தொழிற்துறை போக்குகள் அல்லது உங்கள் தொழில் பயணத்தில் எதையும் பற்றி எனக்குக் கேளுங்கள்."
            try_label = "Try asking:" if lang == "en" else "கேட்க முயற்சி செய்யுங்கள்:"
            
            suggestions = [
                "What skills should I learn first for this role?",
                "How do I transition from my current field?",
                "What does a typical day look like in this role?",
                "How do I prepare for interviews in this domain?",
            ] if lang == "en" else [
                "இந்த பாத்திரத்திற்கு நான் முதலில் என்ன திறன்களைக் கற்க வேண்டும்?",
                "நான் என் தற்போதைய துறையிலிருந்து எவ்வாறு மாறுவது?",
                "இந்த பாத்திரத்தில் ஒரு வழக்கமான நாள் எப்படி இருக்கிறது?",
                "இந்த டொமேயினில் நான் எவ்வாறு பேட்டிக்கு தயாரிகிறது?",
            ]
            
            st.markdown(f"""
            <div class="chat-empty-state">
                <div style="font-size: 3rem;">🤖</div>
                <h4>{ready_msg}</h4>
                <p>{desc_msg}</p>
                <div class="suggested-questions">
                    <strong>{try_label}</strong>
                    <ul>
                        <li>"{suggestions[0]}"</li>
                        <li>"{suggestions[1]}"</li>
                        <li>"{suggestions[2]}"</li>
                        <li>"{suggestions[3]}"</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state["chat_messages"]:
                role = msg["role"]
                content = msg["content"]
                with st.chat_message(role):
                    st.markdown(content)

    # ── Chat Input ────────────────────────────────────────────────────────────
    input_placeholder = "Ask your career mentor anything..." if lang == "en" else "உங்கள் தொழில் மெண்டரிடம் எதையும் கேளுங்கள்..."
    
    user_input = st.chat_input(
        input_placeholder,
        key="chat_input"
    )

    if user_input:
        # Append user message
        st.session_state["chat_messages"].append({
            "role": "user",
            "content": user_input
        })

        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate response
        with st.chat_message("assistant"):
            thinking_msg = "Thinking..." if lang == "en" else "சிந்தித்துக்கொண்டிருக்கிறது..."
            with st.spinner(thinking_msg):
                system_prompt = get_chat_system_prompt(
                    career_domain or "General Career Development"
                )
                response = query_model(system_prompt, user_input)
            st.markdown(response)

        # Save assistant message
        st.session_state["chat_messages"].append({
            "role": "assistant",
            "content": response
        })
