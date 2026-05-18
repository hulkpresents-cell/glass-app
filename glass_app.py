import streamlit as st
import random
from docx import Document
import io

# Page configuration
st.set_page_config(
    page_title="AuraGen - Smart Word File Reader",
    page_icon="📄",
    layout="wide"
)

# PREMIUM GLASSMORPHISM CSS
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(20, 16, 45, 1) 0%, rgba(13, 10, 31, 1) 40%, rgba(26, 12, 48, 1) 75%, rgba(8, 6, 21, 1) 100%) !important;
        background-attachment: fixed !important;
        color: #e2e8f0 !important;
    }
    h1, h2, h3, p, label { color: #f8fafc !important; }
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
    .stButton>button {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.6) 0%, rgba(99, 102, 241, 0.6) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
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
        border-bottom: 1px solid #94a3b8;
        padding-bottom: 8px;
    }
    .question-item {
        margin-bottom: 15px;
        display: flex;
        justify-content: space-between;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div style='text-align: center;'><h1>✨ AuraGen: Smart Word File Reader</h1><p>আপনার .docx ফাইল থেকে সরাসরি প্রশ্নপত্র তৈরি করুন</p></div>", unsafe_allow_html=True)

# File Uploader focused on DOCX
uploaded_file = st.file_uploader("📂 আপনার প্রশ্নব্যাংক (.docx ফাইল) এখানে আপলোড করুন", type=["docx"])

if uploaded_file is not None:
    all_questions = []
    
    try:
        # Secure memory layout using bytes io
        doc = Document(io.BytesIO(uploaded_file.read()))
        for para in doc.paragraphs:
            line = para.text.strip()
            # If line has text and looks like a question or valid point
            if len(line) > 3:
                all_questions.append(line)
    except Exception as e:
        st.error("❌ ফাইলটি প্রসেস করতে সমস্যা হয়েছে। দয়া করে নিশ্চিত করুন ফাইলটি সঠিকভাবে .docx ফরম্যাটে সেভ করা।")

    if all_questions:
        st.success(f"✅ আপনার ফাইল থেকে সফলভাবে {len(all_questions)} টি লাইন/প্রশ্ন লোড হয়েছে!")
        
        col_config, col_preview = st.columns([1, 1.8], gap="large")
        
        with col_config:
            st.markdown("### ⚙️ কনফিগারেশন")
            school_name = st.text_input("🏫 শিক্ষা প্রতিষ্ঠানের নাম", value="NOAKHALI SCIENCE & TECHNOLOGY UNIVERSITY")
            exam_name = st.text_input("📝 পরীক্ষার নাম", value="ANNUAL EVALUATION / TERM TEST")
            subject_name = st.text_input("📖 বিষয়ের নাম (Subject)", value="Chemistry")
            
            num_questions = st.number_input("📊 কয়টি প্রশ্ন সিলেক্ট করতে চান?", min_value=1, max_value=len(all_questions), value=min(10, len(all_questions)))
            generate_btn = st.button("🚀 প্রশ্নপত্র তৈরি করুন")
            
        with col_preview:
            st.markdown("### 👁️ প্রশ্নপত্র প্রিভিউ")
            
            if generate_btn:
                selected_qs = random.sample(all_questions, int(num_questions))
                
                paper_html = '<div class="exam-paper-container">'
                paper_html += f"""
                <div class="exam-header">
                    <h2>{school_name.upper()}</h2>
                    <h3>{exam_name.upper()}</h3>
                </div>
                <div class="exam-metadata">
                    <div>Subject: {subject_name}</div>
                    <div>Total Questions: {num_questions}</div>
                </div>
                """
                
                for i, q in enumerate(selected_qs, 1):
                    paper_html += f"""
                    <div class="question-item">
                        <div><strong>Q{i}.</strong> {q}</div>
                    </div>
                    """
                paper_html += "</div>"
                st.markdown(paper_html, unsafe_allow_html=True)
else:
    st.info("💡 অ্যাপটি ব্যবহার করতে প্রথমে আপনার মেইন ফাইলটি মোবাইলে .docx ফরম্যাটে Save As করে এখানে আপলোড করুন।")
