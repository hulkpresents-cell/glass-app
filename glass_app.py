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
    # Physics - Class 11 & 12
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
    
    # Chemistry - Class 11 & 12
    {"id": 11, "text": "Explain the mechanism of nucleophilic substitution reactions (SN1 and SN2) in haloalkanes.", "subject": "Chemistry", "class": "12", "chapter": "Organic Chemistry", "marks": 5},
    {"id": 12, "text": "How do you distinguish between primary, secondary, and tertiary alcohols using Lucas reagent?", "subject": "Chemistry", "class": "12", "chapter": "Organic Chemistry", "marks": 5},
    {"id": 13, "text": "Write notes on: (a) Wurtz-Fittig reaction, (b) Friedel-Crafts Alkylation.", "subject": "Chemistry", "class": "12", "chapter": "Organic Chemistry", "marks": 3},
    {"id": 14, "text": "State Henry's law and discuss its major industrial applications.", "subject": "Chemistry", "class": "12", "chapter": "Solutions", "marks": 3},
    {"id": 15, "text": "Define osmotic pressure. Why is it considered a colligative property?", "subject": "Chemistry", "class": "12", "chapter": "Solutions", "marks": 2},
    {"id": 16, "text": "Calculate the molarity of a solution containing 5g of NaOH in 450 mL of water.", "subject": "Chemistry", "class": "12", "chapter": "Solutions", "marks": 2},
    {"id": 17, "text": "State Raoult's law for non-volatile solutes and explain ideal solution behavior.", "subject": "Chemistry", "class": "12", "chapter": "Solutions", "marks": 5},
    
    # Computer Science - Class 11 & 12
    {"id": 18, "text": "Explain the difference between call by value and call by reference parameters with code snippets.", "subject": "Computer Science", "class": "12", "chapter": "Functions", "marks": 5},
    {"id": 19, "text": "What is function overloading? Provide a valid Python or C++ simulation.", "subject": "Computer Science", "class": "12", "chapter": "Functions", "marks": 3},
    {"id": 20, "text": "Define Scope Rules (LEGB rule) in Python with a comprehensive example.", "subject": "Computer Science", "class": "12", "chapter": "Functions", "marks": 2},
    {"id": 21, "text": "Discuss the primary differences between local and global variables.", "subject": "Computer Science", "class": "12", "chapter": "Functions", "marks": 2},
    {"id": 22, "text": "Write a user-defined function to find and return the frequency of all elements in a given list.", "subject": "Computer Science", "class": "12", "chapter": "Functions", "marks": 5},
    {"id": 23, "text": "What is a primary key? How does it differ from a candidate key in RDBMS?", "subject": "Computer Science", "class": "12", "chapter": "Database Concepts", "marks": 3},
    {"id": 24, "text": "Explain SELECT, PROJECT, and JOIN operations in relational algebra.", "subject": "Computer Science", "class": "12", "chapter": "Database Concepts", "marks": 5},
    {"id": 25, "text": "State the advantages of using DBMS over traditional flat file systems.", "subject": "Computer Science", "class": "12", "chapter": "Database Concepts", "marks": 2},
    
    # Class 9 & 10 (Shorter Physics / Chemistry / Science)
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
    /* Premium Ambient Gradient Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(20, 16, 45, 1) 0%, rgba(13, 10, 31, 1) 40%, rgba(26, 12, 48, 1) 75%, rgba(8, 6, 21, 1) 100%) !important;
        background-attachment: fixed !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    }

    /* Style titles & headers */
    h1, h2, h3, h4, h5, h6, p, label {
        color: #f8fafc !important;
        font-weight: 500;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    /* Make block headers stand out with a premium pinkish-purple gradient */
    h1 {
        background: linear-gradient(135deg, #f472b6 0%, #c084fc 50%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.05em;
    }

    /* Target standard Streamlit cards and columns to apply Glassmorphism */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] > div {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(16px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(16px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }

    /* Glass Panels for Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(12, 9, 28, 0.65) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
        box-shadow: 5px 0 25px rgba(0,0,0,0.5) !important;
    }

    /* Custom Glass Box Utility */
    .glass-card {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(20px) saturate(190%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(190%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 30px !important;
        box-shadow: 0 12px 40px 0 rgba(15, 12, 40, 0.5) !important;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }

    /* Subtle internal neon glow lines for cards */
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, rgba(244,114,182,0) 0%, rgba(244,114,182,0.4) 30%, rgba(168,85,247,0.4) 70%, rgba(99,102,241,0) 100%);
    }

    /* Streamlit Selectboxes, Inputs, Sliders Custom Glass UI */
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
        backdrop-filter: blur(10px);
    }
    
    div[data-baseweb="select"] span, div[data-baseweb="select"] svg {
        color: #e2e8f0 !important;
    }

    input, textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
    }

    /* Radio button labels and checkmarks */
    div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 10px 18px !important;
        border-radius: 10px !important;
        transition: all 0.2s ease-in-out;
        margin-bottom: 5px !important;
        display: flex !important;
        align-items: center !important;
    }

    div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(244, 114, 182, 0.3) !important;
    }

    /* Styled Custom Premium Button with Glass Reflex effect */
    .stButton>button {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.6) 0%, rgba(99, 102, 241, 0.6) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        width: 100% !important;
        backdrop-filter: blur(5px);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(168, 85, 247, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.75) 0%, rgba(99, 102, 241, 0.75) 100%) !important;
    }

    .stButton>button:active {
        transform: translateY(1px);
        box-shadow: 0 2px 10px rgba(168, 85, 247, 0.4) !important;
    }

    /* Virtual Document / Exam Paper Sheet Simulator Wrapper */
    .exam-paper-container {
        background: #ffffff !important;
        color: #1e293b !important;
        border-radius: 8px !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.6) !important;
        padding: 40px !important;
        margin: 15px auto !important;
        font-family: 'Times New Roman', Times, serif !important;
        border: 1px solid #cbd5e1 !important;
        position: relative;
    }

    .exam-paper-container h1, 
    .exam-paper-container h2, 
    .exam-paper-container h3, 
    .exam-paper-container h4,
    .exam-paper-container p,
    .exam-paper-container span,
    .exam-paper-container div {
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
        align-items: flex-start;
        font-size: 15px;
        line-height: 1.5;
    }

    .question-text {
        padding-right: 25px;
        text-align: justify;
    }

    .question-marks {
        font-weight: bold;
        white-space: nowrap;
        font-style: italic;
    }

    /* Landscape Sheet Mode Adjustment */
    .landscape-sheet {
        max-width: 95% !important;
        display: grid !important;
        grid-template-columns: 1fr 1fr;
        column-gap: 40px;
        border-right: none;
    }
    
    .landscape-separator {
        position: absolute;
        top: 5%;
        bottom: 5%;
        left: 50%;
        width: 1px;
        border-left: 1px dashed #cbd5e1;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.02);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
    }
</style>
"""
st.markdown(glass_css, unsafe_allow_html=True)


# -------------------------------------------------------------
# HELPER SMART GENERATION FUNCTIONS
# -------------------------------------------------------------
def get_available_filters(pool):
    """Dynamically parses pool to aggregate distinct classes, subjects, and chapters."""
    classes = sorted(list(set(q["class"] for q in pool)))
    subjects = sorted(list(set(q["subject"] for q in pool)))
    return classes, subjects

def get_chapters_for_subject(pool, subject, class_val):
    """Filters unique chapters based on subject and class."""
    chapters = list(set(q["chapter"] for q in pool if q["subject"] == subject and q["class"] == class_val))
    return sorted(chapters)

def assemble_exam_paper(pool, class_val, subject, target_marks, select_chapters):
    """
    Tries to assemble a question paper precisely matching target marks.
    Employs a simple randomized knapsack solver over filtered criteria.
    """
    # Filter base pool
    filtered = [
        q for q in pool 
        if q["class"] == class_val 
        and q["subject"] == subject 
        and q["chapter"] in select_chapters
    ]
    
    if not filtered:
        return [], 0
    
    # Simple backtracking solver to find an exact marks combination
    best_combination = []
    best_sum = 0
    
    # We attempt 150 random assemblies to find an exact match, fallback to closest
    for _ in range(150):
        shuffled = list(filtered)
        random.shuffle(shuffled)
        
        current_selection = []
        current_sum = 0
        
        for q in shuffled:
            if current_sum + q["marks"] <= target_marks:
                current_selection.append(q)
                current_sum += q["marks"]
            if current_sum == target_marks:
                break
                
        if current_sum == target_marks:
            # Found exact match
            return current_selection, current_sum
        elif current_sum > best_sum:
            best_combination = current_selection
            best_sum = current_sum
            
    return best_combination, best_sum


# -------------------------------------------------------------
# MAIN APP INTERFACE
# -------------------------------------------------------------

# Title Header & Premium Banner
st.markdown("""
<div class="glass-card" style="text-align: center; padding: 40px 20px;">
    <h1>✨ AuraGen: Glassmorphic Question Paper Generator</h1>
    <p style="font-size: 1.15rem; color: #cbd5e1; max-width: 750px; margin: 10px auto auto auto; line-height: 1.6;">
        Generate and preview high-fidelity customized academic assessments. Configure your variables below to compile structured exams instantly with elegant templates.
    </p>
</div>
""", unsafe_allow_html=True)

# Fetch current dynamic pools from database
db_classes, db_subjects = get_available_filters(QUESTION_POOL)

# Create layout containing Sidebar Configuration and Preview Area
col_config, col_preview = st.columns([1, 1.8], gap="large")

with col_config:
    st.markdown("""
    <div class="glass-card">
        <h3 style="margin-top:0; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; display: flex; align-items: center; gap: 10px;">
            ⚙️ Configuration Toggles
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Class Select
    selected_class = st.selectbox(
        "🎯 Select Academic Class",
        options=db_classes,
        index=db_classes.index("12") if "12" in db_classes else 0,
        help="Filters question database for appropriate student grade level."
    )
    
    # Subject Select
    selected_subject = st.selectbox(
        "📖 Target Subject",
        options=db_subjects,
        index=0,
        help="Subject scope of the exam."
    )
    
    # Dynamic Chapter Selection
    available_chapters = get_chapters_for_subject(QUESTION_POOL, selected_subject, selected_class)
    
    if available_chapters:
        selected_chapters = st.multiselect(
            "🗂️ Select Chapters to Include",
            options=available_chapters,
            default=available_chapters,
            help="Extract questions originating only from these selected chapters."
        )
    else:
        st.warning("⚠️ No questions matching this Class + Subject combination in current simulation database.")
        selected_chapters = []
        
    # Total Marks Radio Toggle
    total_marks = st.radio(
        "📊 Target Total Marks",
        options=[40, 50, 70, 100],
        index=1,
        horizontal=True,
        help="AuraGen smart solver will pick items perfectly matching this point distribution."
    )
    
    # Custom Smart Auto-Recommendation for Sheet Layout
    default_layout_index = 0 if total_marks <= 40 else 1
    
    # Visual Page Layout / Sheet Configuration radio
    layout_config = st.radio(
        "🖨️ Simulated Page/Sheet Layout Configuration",
        options=[
            "Two-in-One Sheet (Landscape)",
            "Single Sheet (Portrait)"
        ],
        index=default_layout_index,
        help="Landscape option splits the exam paper into double columns to simulate space-saving double-sided booklets."
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action Button
    generate_btn = st.button("🚀 Generate Question Paper")

with col_preview:
    st.markdown("""
    <div class="glass-card" style="height: 100%;">
        <h3 style="margin-top:0; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;">
            👁️ Exam Paper Sheet Preview (Live Render)
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state placeholders for simulation
    if 'generated_paper' not in st.session_state:
        st.session_state.generated_paper = None
        st.session_state.actual_marks = 0
        st.session_state.metadata = {}

    # Triggered logic execution upon clicking Button
    if generate_btn:
        if not selected_chapters:
            st.error("Please choose at least one chapter to source questions.")
        else:
            with st.spinner("✨ Sourcing database indices and running optimization solver..."):
                time.sleep(0.9)  # Simulated file reading / parsing duration
                
                selected_qs, summed_marks = assemble_exam_paper(
                    QUESTION_POOL, 
                    selected_class, 
                    selected_subject, 
                    total_marks, 
                    selected_chapters
                )
                
                st.session_state.generated_paper = selected_qs
                st.session_state.actual_marks = summed_marks
                st.session_state.metadata = {
                    "class": selected_class,
                    "subject": selected_subject,
                    "target_marks": total_marks,
                    "layout": layout_config
                }
                
                st.toast("✅ Exam paper compiled successfully!", icon="📝")

    # Render Sheet Simulation Card
    if st.session_state.generated_paper:
        meta = st.session_state.metadata
        paper_qs = st.session_state.generated_paper
        act_marks = st.session_state.actual_marks
        
        # Check target marks accuracy
        if act_marks < meta["target_marks"]:
            st.warning(f"💡 Limited question database pool. Assembled closest possible match: **{act_marks} out of {meta['target_marks']} Marks**.")
        else:
            st.success(f"🎯 Successfully assembled exact **{act_marks} Marks** assessment!")
            
        is_landscape = "Landscape" in meta["layout"]
        
        # HTML simulation of standard structural paper sheet
        paper_html = f"""
        <div class="exam-paper-container {'landscape-sheet' if is_landscape else ''}">
        """
        
        # Inner content structure
        inner_content = f"""
            <div class="exam-header">
                <h2 style="font-size: 22px; margin: 0; font-family: 'Times New Roman', serif;">AURA PRESTIGE ACADEMY</h2>
                <h3 style="font-size: 16px; margin: 5px 0 0 0; font-family: 'Times New Roman', serif;">ANNUAL EVALUATION EXAMINATION</h3>
                <p style="font-size: 13px; margin: 2px 0 0 0; font-family: 'Times New Roman', serif;">Session 2026 - 2027</p>
            </div>
            
            <div class="exam-metadata">
                <div>Subject: {meta['subject']} (Class {meta['class']})</div>
                <div>Time Allowed: {"1.5 Hours" if meta['target_marks'] <= 40 else "3 Hours"}</div>
                <div>Max Marks: {meta['target_marks']}</div>
            </div>
            
            <p style="font-size: 13px; font-style: italic; margin-bottom: 20px; font-weight: bold;">
                General Instructions: All questions are compulsory. Use neat diagrams wherever applicable.
            </p>
        """
        
        # Populate dynamic questions
        questions_block = ""
        for index, q in enumerate(paper_qs, start=1):
            questions_block += f"""
            <div class="question-item">
                <div class="question-text">
                    <strong>Q{index}.</strong> {q['text']}
                    <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Source Chapter: {q['chapter']}</div>
                </div>
                <div class="question-marks">[{q['marks']} Marks]</div>
            </div>
            """
            
        if is_landscape:
            # For landscape, duplicate structure in two columns to simulate the 2-in-1 layout
            paper_html += f"""
                <div>
                    {inner_content}
                    {questions_block}
                    <div style="text-align: center; font-size: 11px; border-top: 1px solid #cbd5e1; margin-top: 30px; padding-top: 5px;">
                        --- End of Section A (Page 1) ---
                    </div>
                </div>
                <div class="landscape-separator"></div>
                <div>
                    {inner_content.replace("ANNUAL EVALUATION EXAMINATION", "ANNUAL EVALUATION - STUDENT COPY")}
                    {questions_block}
                    <div style="text-align: center; font-size: 11px; border-top: 1px solid #cbd5e1; margin-top: 30px; padding-top: 5px;">
                        --- End of Section B (Page 2) ---
                    </div>
                </div>
            """
        else:
            # Standard single page portrait layout
            paper_html += f"""
                {inner_content}
                {questions_block}
                <div style="text-align: center; font-size: 12px; margin-top: 40px; border-top: 1px solid #cbd5e1; padding-top: 10px; font-weight: bold;">
                    *** End of Question Paper ***
                </div>
            """
            
        paper_html += "</div>"
        
        # Display Generated Visual Paper
        st.markdown(paper_html, unsafe_allow_html=True)
        
        # Export Actions inside customized premium footer
        st.markdown("<br>", unsafe_allow_html=True)
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.button("📥 Export Compiled exam .DOCX (Simulated)")
        with col_dl2:
            st.button("⚙️ Open Typography and Font Panel")
            
    else:
        # Default placeholder before user clicks action button
        st.markdown("""
        <div style="text-align: center; padding: 100px 20px; border: 2px dashed rgba(255, 255, 255, 0.1); border-radius: 12px; background: rgba(255, 255, 255, 0.01);">
            <p style="font-size: 2.5rem; margin: 0;">📄</p>
            <h4 style="margin: 10px 0 0 0; color: #cbd5e1;">Awaiting Generation</h4>
            <p style="font-size: 0.9rem; color: #64748b; margin-top: 5px;">
                Select academic parameters on the configuration panel and click 'Generate Question Paper' to visualize output here.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer Notes
st.markdown("""
<div style="text-align: center; padding: 40px 0; margin-top: 50px; font-size: 0.85rem; color: #475569; border-top: 1px solid rgba(255,255,255,0.05)">
    AuraGen Engine © 2026. Custom glassmorphic stylesheet styled with ♥ for Streamlit.
</div>
""", unsafe_allow_html=True)Generate a complete, single Python file (say, glass_app.py) for a web application using the Streamlit library. This application should simulate a 'Smart Question Paper Generator' with a specific focus on achieving a high-gloss, premium Glassmorphism (Glassmorphic) UI.
​The application must include the following features and structural elements:
​Backend Logic (Simplified): Create simple functions that read a hypothetical .docx file (use a dummy file path or input text for simulation) and extract questions based on selected attributes. The core logic should filter questions by Class, Subject, and Chapter.
​Configuration Toggles: Implement input widgets (Streamlit's st.selectbox, st.radio, or st.slider) for the following user configurations:
​Total Marks: Options for 40, 50, 70, or 100 marks.
​Page Layout/Sheet Configuration: Use a visual st.radio or buttons with labels like:
​"Two-in-One Sheet (Landscape)" (for 40 marks or less).
​"Single Sheet (Portrait)" (for 50 marks or more).
​Visual Interface (Crucial): Embed custom CSS directly into the Streamlit app to transform the default UI into a modern Glassmorphism theme. The CSS must feature:
​A soft, deep ambient gradient background (e.g., deep sapphire blue to subtle amethyst purple).
​Semi-translucent, heavily blurred (backdrop-filter) panels/containers for the main control section and output preview.
​High-gloss, reflective surfaces on buttons and selected elements (using gradients and border-radius).
​Precise, thin, glowing white borders for panels.
​Action Button and Preview: Include a prominent 'Generate Question Paper' button. Upon clicking, it should display a simulated text preview of the question paper on a separate glassy panel, adhering to the selected configuration.
​Dummy Data for Simulation: For the purpose of demonstration, use dummy Python lists or dictionaries to represent the questions (e.g., 'questions': [{'text': 'Question 1', 'chapter': 'Ch1', 'class': '9', 'marks': 10}, ...]).
​Ensure the code is clean, commented, and ready to be run using streamlit run glass_app.py after saving."
