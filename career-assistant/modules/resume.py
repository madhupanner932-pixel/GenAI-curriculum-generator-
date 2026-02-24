"""
modules/resume.py

Resume Analyzer module — Streamlit UI + logic.
Enhanced with file upload and compression features.
"""

import streamlit as st
import os
import gzip
import shutil
from io import BytesIO
from pathlib import Path
from utils.model import query_model
from prompts.resume_prompt import RESUME_SYSTEM_PROMPT, get_resume_user_prompt

# Try importing file handling libraries
try:
    from PyPDF2 import PdfReader
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    from docx import Document
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False


# Sample resume for quick testing
SAMPLE_RESUME = """John Doe
Email: john.doe@email.com | LinkedIn: linkedin.com/in/johndoe | GitHub: github.com/johndoe

EDUCATION
B.Tech in Computer Science | XYZ University | 2020-2024 | CGPA: 7.8/10

SKILLS
Python, Java, HTML, CSS, MySQL, Basic Machine Learning

PROJECTS
1. Student Management System - Built a CRUD application using Python and MySQL
2. Weather Website - Fetched weather data using OpenWeatherMap API

INTERNSHIP
Web Development Intern | ABC Company | June-August 2023
- Developed 3 web pages using HTML and CSS
- Assisted senior developers with bug fixing

CERTIFICATIONS
- Python for Beginners (Coursera)
- Web Development Bootcamp (Udemy)
"""


def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file."""
    if not HAS_PDF:
        st.error("❌ PDF support not installed. Please run: pip install PyPDF2")
        return None
    
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"❌ Error reading PDF: {str(e)}")
        return None


def extract_text_from_docx(docx_file):
    """Extract text from DOCX file."""
    if not HAS_DOCX:
        st.error("❌ DOCX support not installed. Please run: pip install python-docx")
        return None
    
    try:
        doc = Document(docx_file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        st.error(f"❌ Error reading DOCX: {str(e)}")
        return None


def compress_file(input_file, filename):
    """Compress file using gzip."""
    try:
        output_filename = f"{Path(filename).stem}_compressed.gz"
        
        # Read input file
        with open(input_file, 'rb') as f_in:
            file_data = f_in.read()
        
        # Compress
        compressed_data = BytesIO()
        with gzip.GzipFile(fileobj=compressed_data, mode='wb') as gz:
            gz.write(file_data)
        
        compressed_data.seek(0)
        
        # Calculate compression ratio
        original_size = len(file_data)
        compressed_size = len(compressed_data.getvalue())
        ratio = (1 - compressed_size / original_size) * 100
        
        return compressed_data, output_filename, original_size, compressed_size, ratio
    
    except Exception as e:
        st.error(f"❌ Compression error: {str(e)}")
        return None, None, None, None, None


def decompress_file(gz_file, output_filename):
    """Decompress gzip file."""
    try:
        output_data = BytesIO()
        with gzip.GzipFile(fileobj=gz_file) as gz:
            output_data.write(gz.read())
        
        output_data.seek(0)
        return output_data
    
    except Exception as e:
        st.error(f"❌ Decompression error: {str(e)}")
        return None


def render_resume():
    """Render the Resume Analyzer page."""

    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="module-header">
        <span class="module-icon">📄</span>
        <div>
            <h2>Resume Analyzer</h2>
            <p>Get expert feedback on your resume: skill gaps, missing keywords & improvement suggestions.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Target Role ───────────────────────────────────────────────────────────
    col1, col2 = st.columns([2, 1])
    with col1:
        target_role = st.text_input(
            "🎯 Target Role / Position",
            placeholder="e.g. Data Scientist, Backend Developer, Product Manager...",
            help="All feedback will be tailored to this specific role."
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        load_sample = st.button("📋 Load Sample Resume", use_container_width=True)

    # ── Input Mode Selection ──────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📥 Resume Input Mode")
    
    input_mode = st.radio(
        "Choose how to provide your resume:",
        ["📝 Paste Text", "📁 Upload File", "🗜️ Upload Compressed File"],
        horizontal=True
    )

    resume_text = ""

    # ── Mode 1: Paste Text ────────────────────────────────────────────────────
    if input_mode == "📝 Paste Text":
        st.markdown("#### Paste Your Resume")
        default_text = SAMPLE_RESUME if load_sample else ""

        resume_text = st.text_area(
            "Resume Content",
            value=default_text,
            height=350,
            placeholder="Paste your resume content here (plain text format)...\n\nTip: Copy from your Word/PDF document and paste here.",
            help="Paste the full text of your resume for comprehensive analysis.",
            label_visibility="collapsed"
        )

        # Character count
        char_count = len(resume_text)
        if char_count > 0:
            st.caption(f"📊 {char_count} characters | ~{max(1, char_count // 250)} page(s)")

    # ── Mode 2: Upload File ───────────────────────────────────────────────────
    elif input_mode == "📁 Upload File":
        st.markdown("#### Upload Resume File")
        st.caption("Supported formats: TXT, PDF, DOCX")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["txt", "pdf", "docx"],
            label_visibility="collapsed"
        )

        if uploaded_file:
            file_type = uploaded_file.type
            filename = uploaded_file.name

            # Display file info
            file_size = uploaded_file.size / 1024  # KB
            st.info(f"📄 **File:** {filename} | **Size:** {file_size:.2f} KB | **Type:** {file_type}")

            # Extract text based on file type
            if filename.endswith('.txt'):
                resume_text = uploaded_file.read().decode('utf-8')
            
            elif filename.endswith('.pdf'):
                if HAS_PDF:
                    resume_text = extract_text_from_pdf(uploaded_file)
                else:
                    st.warning("⚠️ PDF support not installed. Install with: `pip install PyPDF2`")
                    resume_text = ""
            
            elif filename.endswith('.docx'):
                if HAS_DOCX:
                    resume_text = extract_text_from_docx(uploaded_file)
                else:
                    st.warning("⚠️ DOCX support not installed. Install with: `pip install python-docx`")
                    resume_text = ""

            if resume_text:
                # Show extracted text preview
                with st.expander("👁️ Preview Extracted Text"):
                    char_count = len(resume_text)
                    st.caption(f"📊 {char_count} characters extracted")
                    st.text_area("Preview", value=resume_text[:500] + "...", height=150, disabled=True)

    # ── Mode 3: Upload Compressed File ────────────────────────────────────────
    elif input_mode == "🗜️ Upload Compressed File":
        st.markdown("#### Upload Compressed Resume (.gz file)")
        
        col_decomp1, col_decomp2 = st.columns(2)
        
        with col_decomp1:
            compressed_file = st.file_uploader(
                "Choose compressed file",
                type=["gz"],
                label_visibility="collapsed"
            )

        if compressed_file:
            file_size = compressed_file.size / 1024
            st.info(f"📦 **Compressed File:** {compressed_file.name} | **Size:** {file_size:.2f} KB")
            
            if st.button("🔓 Decompress & Extract", use_container_width=True):
                decompressed = decompress_file(compressed_file, compressed_file.name)
                if decompressed:
                    # Try to read as text
                    try:
                        resume_text = decompressed.read().decode('utf-8')
                        char_count = len(resume_text)
                        st.success(f"✅ Decompressed successfully! {char_count} characters extracted.")
                        
                        with st.expander("👁️ Preview Decompressed Text"):
                            st.text_area("Preview", value=resume_text[:500] + "...", height=150, disabled=True)
                    
                    except Exception as e:
                        st.error(f"❌ Error reading decompressed file: {str(e)}")

    # ── File Compression Tool ─────────────────────────────────────────────────
    st.markdown("---")
    with st.expander("🗜️ File Compression Tool"):
        st.markdown("#### Compress Your Resume File")
        st.caption("Reduce file size for easier sharing and storage")
        
        file_to_compress = st.file_uploader(
            "Select file to compress",
            type=["pdf", "docx", "txt"],
            key="compress_uploader",
            label_visibility="collapsed"
        )

        if file_to_compress:
            col_c1, col_c2 = st.columns(2)
            
            with col_c1:
                original_size = file_to_compress.size / 1024
                st.metric("Original Size", f"{original_size:.2f} KB")
            
            if st.button("🗜️ Compress File", use_container_width=True, key="compress_btn"):
                # Save temporarily
                temp_path = f"/tmp/{file_to_compress.name}"
                with open(temp_path, 'wb') as f:
                    f.write(file_to_compress.read())

                compressed_data, output_name, orig_size, comp_size, ratio = compress_file(temp_path, file_to_compress.name)

                if compressed_data:
                    with col_c2:
                        compressed_kb = comp_size / 1024
                        st.metric("Compressed Size", f"{compressed_kb:.2f} KB")
                    
                    st.success(f"✅ Compressed! **Saved {ratio:.1f}%** of space")

                    # Download button
                    st.download_button(
                        label="📥 Download Compressed File",
                        data=compressed_data.getvalue(),
                        file_name=output_name,
                        mime="application/gzip",
                        use_container_width=True
                    )

                # Cleanup
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    # ── Analyze Button ────────────────────────────────────────────────────────
    st.markdown("---")
    analyze = st.button(
        "🔍 Analyze My Resume",
        use_container_width=True,
        type="primary",
        disabled=(not resume_text.strip() or not target_role.strip())
    )

    if not resume_text.strip() or not target_role.strip():
        if not target_role.strip():
            st.caption("⚠️ Enter your target role to enable analysis.")
        if not resume_text.strip():
            st.caption("⚠️ Provide your resume (paste or upload) to enable analysis.")

    # ── Analysis ──────────────────────────────────────────────────────────────
    if analyze:
        if len(resume_text.strip()) < 100:
            st.warning("⚠️ Your resume seems very short. Please provide more content for accurate analysis.")
            return

        with st.spinner("🤖 Analyzing your resume in depth..."):
            user_prompt = get_resume_user_prompt(resume_text.strip(), target_role.strip())
            result = query_model(RESUME_SYSTEM_PROMPT, user_prompt)

        st.success("✅ Analysis complete!")
        st.markdown("---")
        st.markdown(result)

        # Download
        st.download_button(
            label="📥 Download Resume Feedback (Markdown)",
            data=result,
            file_name=f"resume_analysis_{target_role.replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    elif not resume_text.strip():
        # Show feature highlights
        st.markdown("""
        <div class="tips-box">
            <h4>📊 What you'll get from your analysis:</h4>
            <ul>
                <li>🎯 <strong>Readiness Score</strong> out of 10 for your target role</li>
                <li>🔍 <strong>ATS Keyword Analysis</strong> — what recruiters are scanning for</li>
                <li>⚠️ <strong>Skill Gap Report</strong> — exactly what's missing</li>
                <li>🛠️ <strong>Improvement Suggestions</strong> — prioritized and actionable</li>
                <li>⚡ <strong>Quick Wins</strong> — changes you can make in under an hour</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
