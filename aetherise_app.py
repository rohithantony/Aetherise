import streamlit as st
import pandas as pd
from fuzzywuzzy import process
import random
import warnings

warnings.filterwarnings("ignore")
st.set_page_config(page_title="Aetherise 🌍", layout="wide")

# ====== Custom CSS ======
st.markdown("""
<style>
    /* Beautiful header styling */
    .main-header {
        color: #4CAF50;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    .sub-header {
        color: #666;
        font-family: 'Roboto', sans-serif;
        font-weight: 300;
        font-style: italic;
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Side panel toggle buttons */
    .toggle-btn {
        position: fixed;
        top: 20px;
        z-index: 100;
        background: #4CAF50 !important;
        color: white !important;
        border-radius: 50% !important;
        width: 40px;
        height: 40px;
        padding: 0 !important;
        min-width: 0 !important;
    }
    .left-toggle {
        left: 10px;
    }
    .right-toggle {
        right: 10px;
    }
    
    /* Side panel animations */
    @keyframes slideInLeft {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
    }
    @keyframes slideOutLeft {
        from { transform: translateX(0); }
        to { transform: translateX(-100%); }
    }
    @keyframes slideInRight {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }
    @keyframes slideOutRight {
        from { transform: translateX(0); }
        to { transform: translateX(100%); }
    }
    .left-panel {
        animation: slideInLeft 0.3s forwards;
    }
    .right-panel {
        animation: slideInRight 0.3s forwards;
    }
    .left-panel.hidden {
        animation: slideOutLeft 0.3s forwards;
    }
    .right-panel.hidden {
        animation: slideOutRight 0.3s forwards;
    }
    
    /* Chat container styling */
    .chat-container {
        transition: all 0.3s ease;
    }
    .left-hidden .chat-container {
        margin-left: 0 !important;
    }
    .right-hidden .chat-container {
        margin-right: 0 !important;
    }
</style>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&family=Roboto:wght@300&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ====== Load Data ======
@st.cache_data
def load_data():
    df = pd.read_excel("Climate_Change_Chatbot_Questions.xlsx")
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_data()
all_questions = df['question'].tolist()

# ====== Initialize Chat State ======
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "left_panel_visible" not in st.session_state:
    st.session_state.left_panel_visible = True
if "right_panel_visible" not in st.session_state:
    st.session_state.right_panel_visible = True

# ====== Toggle Buttons ======
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("◄", key="left_toggle", help="Toggle left panel"):
        st.session_state.left_panel_visible = not st.session_state.left_panel_visible
with col3:
    if st.button("►", key="right_toggle", help="Toggle right panel"):
        st.session_state.right_panel_visible = not st.session_state.right_panel_visible

# ====== Layout Structure ======
main_container = st.container()
left_col, center_col, right_col = st.columns([0.2, 0.55, 0.25])

# ====== Left Sidebar: Trusted Links ======
left_panel_class = "" if st.session_state.left_panel_visible else "hidden"
with left_col:
    st.markdown(f'<div class="left-panel {left_panel_class}">', unsafe_allow_html=True)
    st.markdown("### 🔗 Trusted Topics")
    topics = sorted(df['topic'].unique())
    selected_topic = st.selectbox("Choose a topic", ["-- Select a topic --"] + topics)

    if selected_topic != "-- Select a topic --":
        links = df[df['topic'] == selected_topic]['trusted links'].unique().tolist()[:5]
        st.markdown("#### 🔍 Trusted Links")
        for link in links:
            st.markdown(f"[🔹 {link}]({link})")
    st.markdown('</div>', unsafe_allow_html=True)

# ====== Center Column: Title + Chat UI ======
with center_col:
    # Beautiful header
    st.markdown("""
    <div style='text-align: center;'>
        <h1 class="main-header">🌍 AETHERISE</h1>
        <p class="sub-header">Your Climate Knowledge Educator 💬</p>
        <hr style='margin: 5px 0 15px 0;'>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    with chat_container:
        for chat in st.session_state.chat_history:
            bubble_color = "#2f2f2f"
            bubble_style = f"background-color: {bubble_color}; padding: 10px 15px; border-radius: 10px; margin: 8px 0px; color: white;"

            alignment = "right" if chat["role"] == "user" else "left"
            prefix = "🟢 You:" if chat["role"] == "user" else "🔵 Aetherise:"
            st.markdown(f"""
            <div style='text-align: {alignment};'>
                <div style='{bubble_style}; display: inline-block; max-width: 80%;'>
                    <strong>{prefix}</strong><br>{chat['text']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Input field
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(" ", value=st.session_state.user_input, 
                                 placeholder="Type your climate question...",
                                 label_visibility="collapsed")
        submit_button = st.form_submit_button("Send")

    if submit_button and user_input.strip():
        def answer_query(user_query):
            match, score = process.extractOne(user_query, all_questions)
            if score > 80:
                row = df[df['question'] == match].iloc[0]
                topic_links = df[df['topic'] == row['topic']]['trusted links'].unique().tolist()[:3]
                return row['answer'], row['topic'], topic_links
            else:
                fallback = ("❓ Sorry, I couldn't find an exact answer in my knowledge base.\n\n"
                            "Try rephrasing your question or explore topics like:\n"
                            "- Greenhouse Effect\n- Climate Change\n- Carbon Footprint\n- Renewable Energy\n\n"
                            "💡 Learn more at:\n"
                            "- https://climate.nasa.gov\n"
                            "- https://www.ipcc.ch\n"
                            "- https://www.un.org/en/climatechange")
                return fallback, None, []

        answer, topic, links = answer_query(user_input.strip())
        st.session_state.chat_history.append({"role": "user", "text": user_input.strip()})
        st.session_state.chat_history.append({"role": "bot", "text": answer})
        st.session_state.user_input = ""
        st.rerun()

# ====== Right Column: Suggestions + Facts ======
right_panel_class = "" if st.session_state.right_panel_visible else "hidden"
with right_col:
    st.markdown(f'<div class="right-panel {right_panel_class}">', unsafe_allow_html=True)
    st.markdown("### 🌟 Did You Know?")
    did_you_know_facts = [
        "The Earth has warmed about 1.1°C since the late 19th century.",
        "Methane is over 25 times more effective than CO₂ at trapping heat in the atmosphere.",
        "Trees can absorb up to 48 pounds of CO₂ per year!",
        "The Arctic is warming nearly four times faster than the rest of the world.",
        "Electric vehicles produce significantly fewer emissions over their lifetime than gas-powered ones."
    ]
    st.info(random.choice(did_you_know_facts))

    st.markdown("### 🧪 Try asking:")
    sample_qs = random.sample(all_questions, 5)
    for q in sample_qs:
        st.markdown(f"- {q}")
    st.markdown('</div>', unsafe_allow_html=True)

# ====== Footer ======
st.markdown("""
<hr>
<div style='text-align: center; color: gray;'>
    Made with 💚 by Rohith using Streamlit | Stay informed. Stay green. 🌿
</div>
""", unsafe_allow_html=True)

# ====== JavaScript for Panel Toggles ======
st.markdown(f"""
<script>
    // Apply initial classes based on panel visibility
    document.addEventListener('DOMContentLoaded', function() {{
        const leftPanel = document.querySelector('.left-panel');
        const rightPanel = document.querySelector('.right-panel');
        
        if ({str(st.session_state.left_panel_visible).lower()}) {{
            leftPanel.classList.remove('hidden');
        }} else {{
            leftPanel.classList.add('hidden');
        }}
        
        if ({str(st.session_state.right_panel_visible).lower()}) {{
            rightPanel.classList.remove('hidden');
        }} else {{
            rightPanel.classList.add('hidden');
        }}
    }});
</script>
""", unsafe_allow_html=True)