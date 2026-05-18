import streamlit as st
import random
import time

# Set page configuration to wide layout with custom title
st.set_page_config(
    page_title="AuraGen - Smart Glassmorphic Exam Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# DUMMY DATABASE (Simulating extracted DOCX data)
# -------------------------------------------------------------
QUESTION_POOL = [
    {"id": 1, "text": "Explain the working principle of a Van de Graaff generator with a neat diagram.", "subject": "Physics", "class": "12", "chapter": "Electrostatics", "marks": 5},
    {"id": 2, "text": "Derive an expression for the electric field intensity due to an electric dipole at an axial point.", "subject": "Physics", "class": "12", "chapter": "Electrostatics", "marks": 5},
    {"id": 3, "text": "State and prove Gauss's Theorem in electrostatics.", "subject": "Physics", "class": "12", "chapter": "Electrostatics", "marks": 3},
    {"id": 4, "text": "Define Electric Flux. Is it a scalar or vector quantity?", "subject": "Physics", "class": "12", "chapter": "Electrostatics", "marks": 2},
    {"id": 5, "text": "What is the capacitance of a parallel plate capacitor when a dielectric slab is introduced?", "subject": "Physics", "class": "12", "chapter": "Electrostatics", "marks": 3},
    {"id": 6, "text": "Define Drift Velocity and derive its relation with electrical conductivity.", "subject": "Physics", "class": "12", "chapter": "Current Electricity", "marks": 5},
    {"id": 7, "text": "State Kirchhoff's Rules. Discuss their physical significance.", "subject": "Physics", "class": "12", "chapter": "Current Electricity", "marks": 3},
    {"id": 8, "text": "What is a Wheatstone bridge? State its balancing condition.", "subject": "Physics", "class": "12", "chapter": "Current Electricity", "marks": 2},
    {"id": 9, "text": "Explain the principle and working of a potentiometer.", "subject": "Physics", "class": "12", "chapter": "Current Electricity", "marks": 5},
    {"id": 10, "text": "Compare resistance and resistivity of a conductor.", "subject": "Physics", "class": "12", "chapter": "Current Electricity", "marks": 2},
    {"id": 11, "text": "Explain the mechanism of nucleophilic substitution reactions (SN1 and SN2) in haloalkanes.", "subject": "Chemistry", "class": "12", "chapter": "Organic Chemistry", "marks": 5},
    {"id": 12, "text": "How do you distinguish between primary, secondary, and tertiary alcohols using Lucas reagent?", "subject": "Chemistry", "class": "12", "chapter": "Organic Chemistry", "marks": 5},
    {"id": 13, "text": "Write notes on: (a) Wurtz-Fittig reaction, (b) Friedel-Crafts Alkylation.", "subject": "Chemistry", "class": "12", "chapter": "Organic Chemistry", "marks": 3},
    {"id": 14, "text": "State Henry's law and discuss its major industrial applications.", "subject": "Chemistry", "class": "12", "chapter": "Solutions", "marks": 3},
    {"id": 15, "text": "Define osmotic pressure. Why is it considered a colligative property?", "subject": "Chemistry", "class": "12", "chapter": "Solutions", "marks": 2},
    {"id": 16, "text": "Calculate the molarity of a solution containing 5g of NaOH in 450 mL of water.", "subject": "Chemistry", "class": "12", "chapter": "Solutions", "marks": 2},
    {"id": 17, "text": "State Raoult's law for non-volatile solutes and explain ideal solution behavior.", "subject": "Chemistry", "class": "12", "chapter": "Solutions", "marks": 5},
    {"id": 18, "text": "Explain the difference between call by value and call by reference parameters with code snippets.", "subject": "Computer Science", "class": "12", "chapter": "Functions", "marks": 5},
    {"id": 19, "text": "What is function overloading? Provide a valid Python simulation.", "subject": "Computer Science", "class": "12", "chapter": "Functions", "marks": 3},
    {"id": 20, "text": "Define Scope Rules (LEGB rule) in Python with a comprehensive example.", "subject": "Computer Science", "class": "12", "chapter": "Functions", "marks": 2},
    {"id": 21, "text": "Discuss the primary differences between local and global variables.", "subject": "Computer Science", "class": "12", "chapter": "Functions", "marks": 2},
    {"id": 22, "text": "Write a user-defined function to find and return the frequency of all elements in a given list.", "subject": "Computer Science", "class": "12", "chapter": "Functions", "marks": 5},
    {"id": 23, "text": "What is a primary key? How does it differ from a candidate key in RDBMS?", "subject": "Computer Science", "class": "12", "chapter": "Database Concepts", "marks": 3},
    {"id": 24, "text": "Explain SELECT, PROJECT, and JOIN operations in relational algebra.", "subject": "Computer Science", "class": "12", "chapter": "Database Concepts", "marks": 5},
    {"id": 25, "text": "State the advantages of using DBMS over traditional flat file systems.", "subject": "Computer Science", "class": "12", "chapter": "Database Concepts", "marks": 2},
    {"id": 26, "text": "State Newton's three laws of motion with real-life application examples.", "subject": "Physics", "class": "9", "chapter": "Laws of Motion", "marks": 5},
    {"id": 27, "text": "Define momentum. Prove that the rate of change of momentum is directly proportional to applied force.", "subject": "Physics", "class": "9", "chapter": "Laws of Motion", "marks": 5},
    {"id": 28, "text": "What is inertia? Name its different types and explain briefly.", "subject": "Physics", "class": "9", "chapter": "Laws of Motion", "marks": 3},
    {"id": 29, "text": "Define balanced and unbalanced forces. Provide one diagnostic example of each.", "subject": "Physics", "class": "9", "chapter": "Laws of Motion", "marks": 2},
    {"id": 30, "text": "Explain why it is advised to tie any luggage kept on the roof of a bus with a rope.", "subject": "Physics", "class": "9", "chapter": "Laws of Motion", "marks": 2},
]

# -------------------------------------------------------------
# THEME INJECTION (Premium Glassmorphism CSS Stylesheet)
# -------------------------------------------------------------
glass_css = """
<style>
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(20, 16, 45, 1) 0%, rgba(13, 10, 31, 1) 40%, rgba(26, 12, 48, 1) 75%, rgba(8, 6, 21, 1) 100%) !important;
        background-attachment: fixed !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        color: #f8fafc !important;
        font-weight: 500;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    h1 {
        background: linear-gradient(135deg, #f472b6 0%, #c084fc 50%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.05em;
    }
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] > div {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(16px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(16px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }
    section[data-testid="stSidebar"] {
        background: rgba(12, 9, 28, 0.65) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(20px) saturate(190%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(190%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 30px !important;
        margin-bottom: 25px;
        position: relative;
    }
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] svg {
        color: #e2e8f0 !important;
    }
    div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 10px 18px !important;
        border-radius: 10px !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.6) 0%, rgba(99, 102, 241, 0.6) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        width: 100% !important;
    }
    .exam-paper-container {
        background: #ffffff !important;
        color: #1e293b !important;
        border-radius: 8px !important;
        padding: 40px !important;
        font-family: 'Times New Roman', Times, serif !important;
        border: 1px solid #cbd5e1 !important;
    }
    .exam-paper-container h1, .exam-paper-container h2, .exam-paper-container h3, .exam-paper-container p, .exam-paper-container span, .exam-paper-container div {
        color: #1e293b !important;
        text-shadow: none !important;
        -webkit-text-fill-color: initial !important;
    }
    .exam-header {
        text-align: center;
        border-bottom: 2px double #334155;
        padding-bottom: 15px;
        margin-bottom: 25px;
    }
    .exam-metadata {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
        font-weight: bold;
        font-size: 14px;
        border-bottom: 1px solid #94a3b8;
        padding-bottom: 8px;
    }
    .question-item {
        margin-bottom: 18px;
        display: flex;
        justify-content: space-between;
    }
    .landscape-sheet {
        display: grid !important;
        grid-template-columns: 1fr 1fr;
        column-gap: 40px;
    }
</style>
"""
st.markdown(glass_css, unsafe_allow_html=True)

# -------------------------------------------------------------
# MAIN APP INTERFACE
# -------------------------------------------------------------
st.markdown("""
<div class="glass-card" style="text-align: center;">
    <h1>✨ AuraGen: Glassmorphic Question Paper Generator</h1>
    <p style="color: #cbd5e1;">Configure your variables below to compile structured exams instantly.</p>
</div>
""", unsafe_allow_html=True)

db_classes = ["9", "12"]
db_subjects = ["Physics", "Chemistry", "Computer Science"]

col_config, col_preview = st.columns([1, 1.8], gap="large")

with col_config:
    st.markdown("### ⚙️ Configuration Toggles")
    selected_class = st.selectbox("🎯 Select Academic Class", options=db_classes, index=1)
    selected_subject = st.selectbox("📖 Target Subject", options=db_subjects, index=0)
    
    available_chapters = list(set(q["chapter"] for q in QUESTION_POOL if q["subject"] == selected_subject and q["class"] == selected_class))
    selected_chapters = st.multiselect("🗂️ Select Chapters", options=available_chapters, default=available_chapters)
    
    total_marks = st.radio("📊 Target Total Marks", options=[40, 50, 70, 100], index=1, horizontal=True)
    layout_config = st.radio("🖨️ Layout Configuration", options=["Two-in-One Sheet (Landscape)", "Single Sheet (Portrait)"], index=1)
    
    generate_btn = st.button("🚀 Generate Question Paper")

with col_preview:
    st.markdown("### 👁️ Exam Paper Sheet Preview")
    
    if generate_btn:
        filtered = [q for q in QUESTION_POOL if q["class"] == selected_class and q["subject"] == selected_subject and q["chapter"] in selected_chapters]
        
        selected_qs = []
        current_sum = 0
        random.shuffle(filtered)
        
        for q in filtered:
            if current_sum + q["marks"] <= total_marks:
                selected_qs.append(q)
                current_sum += q["marks"]
                
        if not selected_qs:
            st.info("No questions generated or filters empty.")
        else:
            is_landscape = "Landscape" in layout_config
            paper_class = "exam-paper-container landscape-sheet" if is_landscape else "exam-paper-container"
            
            st.success(f"🎯 Total Marks Matched: {current_sum}/{total_marks}")
            
            paper_html = f'<div class="{paper_class}">'
            
            def render_content(title_suffix=""):
                content = f"""
                <div class="exam-header">
                    <h2>AURA PRESTIGE ACADEMY</h2>
                    <h3>ANNUAL EVALUATION {title_suffix}</h3>
                    <p>Session 2026 - 2027</p>
                </div>
                <div class="exam-metadata">
                    <div>Subject: {selected_subject} (Class {selected_class})</div>
                    <div>Max Marks: {total_marks}</div>
                </div>
                """
                for i, q in enumerate(selected_qs, 1):
                    content += f"""
                    <div class="question-item">
                        <div><strong>Q{i}.</strong> {q['text']}</div>
                        <div><i>[{q['marks']} M]</i></div>
                    </div>
                    """
                return content

            if is_landscape:
                paper_html += f"<div>{render_content('PART-A')}</div><div>{render_content('PART-B')}</div>"
            else:
                paper_html += render_content("EXAMINATION")
                
            paper_html += "</div>"
            st.markdown(paper_html, unsafe_allow_html=True)
