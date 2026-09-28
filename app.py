import streamlit as st
import os
from pypdf import PdfReader
import google.generativeai as genai

# Page Configuration
st.set_page_config(
    page_title="AI Resume Analyzer", 
    page_icon="📄", 
    layout="wide"
)

# Sidebar Configuration for API Key
st.sidebar.header("🔑 API Configuration")
api_key = st.sidebar.text_input("Enter your Google Gemini API Key", type="password")

st.title("📄 AI Resume Analyzer & Job Matcher")
st.markdown("Upload your resume (PDF) and paste a target Job Description to get an instant AI evaluation, matching score, and missing skills breakdown.")

# Main Layout Columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF resume file", type=["pdf"])

with col2:
    st.subheader("2. Job Description")
    job_description = st.text_area("Paste the Job Description here...", height=150)

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Analysis Action Button
if st.button("🚀 Analyze Resume", type="primary"):
    if not api_key:
        st.error("Please enter your Google Gemini API key in the sidebar.")
    elif not uploaded_file:
        st.error("Please upload a resume PDF file.")
    elif not job_description:
        st.error("Please provide a job description.")
    else:
        with st.spinner("Extracting text and analyzing with AI..."):
            try:
                # Configure Gemini API
                genai.configure(api_key=api_key)
                
                # Extract text from uploaded PDF
                resume_text = extract_text_from_pdf(uploaded_file)
                
                # Construct Professional Prompt
                prompt = f"""
                You are an expert HR Manager, ATS (Applicant Tracking System) specialist, and Technical Recruiter. 
                Analyze the following resume against the provided job description.
                
                Resume Text:
                {resume_text}
                
                Job Description:
                {job_description}
                
                Provide a detailed evaluation report structured with the following sections:
                1. **Match Percentage**: An estimated match score out of 100% based on skills and requirements.
                2. **Identified Key Skills**: List the core technical and soft skills found in the resume.
                3. **Missing Skills**: Critical skills or requirements mentioned in the Job Description that are missing from the resume.
                4. **Improvement Suggestions**: Actionable, bulleted recommendations to optimize and tailor the resume for this specific role.
                """
                
                # Generate Content using Gemini
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                
                st.success("Analysis Complete!")
                st.markdown("---")
                st.markdown("### 📊 AI Evaluation Report")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")