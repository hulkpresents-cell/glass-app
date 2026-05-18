import streamlit as st
import random
import time
from docx import Document
import io

# Page configuration for a premium dark feel
st.set_page_config(
    page_title="AuraGen - Smart Docx Paper Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# THEME INJECTION (Premium Glassmorphism CSS)
# -------------------------------------------------------------
glass_css = """
<style>
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(20, 16, 45, 1) 0%, rgba(13, 10, 31, 1) 40%, rgba(26, 12, 48, 1) 75%, rgba(8, 6, 21, 1) 100%) !important;
        background-attachment: fixed !important;
        color: #e2e8f0 !important;
        font-family: system-ui, -apple-system, sans-serif !important;
    }
    h1, h2, h3, h4, p, label {
        color: #f8fafc !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    h1 {
        background: linear-gradient(135deg, #f472b6 0%, #c084fc 50%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] > div {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(16px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 24px !important;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        margin-bottom: 25px;
    }
    .stButton>button {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.6) 0%, rgba(99, 102, 241, 0.6) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
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
    .exam-paper-container h2, .exam-paper-container h3, .exam-paper-container p, .exam-paper-container div {
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
# DOCX PARSER ENGINE
# -------------------------------------------------------------
def parse_docx_questions(file_bytes):
    """
    নিয়ম: আপনার .docx ফাইলের প্রতি লাইনে একটি প্রশ্ন এভাবে থাকতে হবে:
    প্রশ্ন লেখা | Subject | Class | Chapter | Marks
    উদাহরণ: হোয়াট ইজ কম্পিউটার? | Computer Science | 12 | Functions | 5
    """
    questions = []
    doc = Document(io.BytesIO(file_bytes))
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text or "|" not in text:
            continue
        
        parts = [p.strip() for p in text.split("|")]
        if len(parts) >= 5:
            try:
                questions.append({
                    "text": parts[0],
                    "subject": parts[1],
                    "class": parts[2],
                    "chapter": parts[3],
                    "marks": int(parts[4])
                })
            except ValueError:
                continue
    return questions

# -------------------------------------------------------------
# APP UI
# -------------------------------------------------------------
st.markdown("""
<div class="glass-card" style="text-align: center;">
    <h1>✨ AuraGen: Smart File-Based Question Generator</h1>
    <p style="color: #cbd5e1;">আপনার নিজের .docx ফাইল আপলোড করে এক ক্লিকে প্রশ্নপত্র তৈরি করুন</p>
</div>
""", unsafe_allow_html=True)

# File Uploader Widget
uploaded_file = st.file_uploader("📂 আপনার প্রশ্নব্যাংক (.docx ফাইল) এখানে আপলোড করুন", type=["docx"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    pool = parse_docx_questions(file_bytes)
    
    if not pool:
        st.error("❌ ফাইলে সঠিক ফরম্যাটে কোনো প্রশ্ন পাওয়া যায়নি! ফাইলে প্রতি লাইনে এভাবে লিখুন: 'প্রশ্ন | Subject | Class | Chapter | Marks'")
    else:
        st.success(f"✅ ফাইল থেকে সফলভাবে {len(pool)} টি প্রশ্ন লোড হয়েছে!")
        
        # Extract Dynamic Filters from uploaded file
        db_classes = sorted(list(set(q["class"] for q in pool)))
        db_subjects = sorted(list(set(q["subject"] for q in pool)))
        
        col_config, col_preview = st.columns([1, 1.8], gap="large")
        
        with col_config:
            st.markdown("### ⚙️ ফিল্টার ও কনফিগারেশন")
            selected_class = st.selectbox("🎯 Class সিলেক্ট করুন", options=db_classes)
            selected_subject = st.selectbox("📖 Subject সিলেক্ট করুন", options=db_subjects)
            
            available_chapters = sorted(list(set(q["chapter"] for q in pool if q["subject"] == selected_subject and q["class"] == selected_class)))
            selected_chapters = st.multiselect("🗂️ Chapter সিলেক্ট করুন", options=available_chapters, default=available_chapters)
            
            total_marks = st.radio("📊 মোট নম্বর (Total Marks)", options=[40, 50, 70, 100], index=1, horizontal=True)
            layout_config = st.radio("🖨️ লেআউট কনফিগারেশন", options=["Two-in-One Sheet (Landscape)", "Single Sheet (Portrait)"], index=1)
            
            generate_btn = st.button("🚀 প্রশ্নপত্র তৈরি করুন")
            
        with col_preview:
            st.markdown("### 👁️ প্রশ্নপত্র প্রিভিউ")
            
            if generate_btn:
                filtered = [q for q in pool if q["class"] == selected_class and q["subject"] == selected_subject and q["chapter"] in selected_chapters]
                
                selected_qs = []
                current_sum = 0
                random.shuffle(filtered)
                
                for q in filtered:
                    if current_sum + q["marks"] <= total_marks:
                        selected_qs.append(q)
                        current_sum += q["marks"]
                
                if not selected_qs:
                    st.info("⚠️ এই ফিল্টারের অধীনে কোনো প্রশ্ন মেলানো সম্ভব হয়নি। দয়া করে অন্য চ্যাপ্টার বা মার্কস ট্রাই করুন।")
                else:
                    is_landscape = "Landscape" in layout_config
                    paper_class = "exam-paper-container landscape-sheet" if is_landscape else "exam-paper-container"
                    
                    st.success(f"🎯 সফলভাবে {current_sum}/{total_marks} মার্কসের প্রশ্ন সেট করা হয়েছে!")
                    
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
else:
    st.info("💡 অ্যাপটি ব্যবহার করতে প্রথমে উপরে আপনার প্রশ্ন ব্যাংকের একটি .docx ফাইল আপলোড করুন।")
