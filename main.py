import streamlit as st
import ollama
import chromadb

from pypdf import PdfReader


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume Builder and Analyzer",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🤖 AI Resume Builder and Analyzer")

st.write(
    "Build and analyze your resume using Local AI "
    "with Ollama and Llama 3.2."
)


# ============================================================
# CHROMADB
# ============================================================

@st.cache_resource
def get_database():

    client = chromadb.Client()

    collection = client.get_or_create_collection(
        name="resume_collection"
    )

    return collection


collection = get_database()


# ============================================================
# OLLAMA
# ============================================================

def ask_llama(prompt):

    try:

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:

        return f"""
### Ollama Error

{str(e)}

Make sure Ollama is running and that `llama3.2`
is installed.
"""


# ============================================================
# PDF READER
# ============================================================

def extract_pdf_text(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📌 Menu")

option = st.sidebar.radio(
    "Select an option",
    [
        "🏠 Home",
        "📝 Build Resume",
        "🔍 Analyze Resume"
    ]
)


# ============================================================
# HOME
# ============================================================

if option == "🏠 Home":

    st.header("Welcome to AI Resume Builder and Analyzer")

    st.write(
        "This application helps users create professional "
        "resumes and analyze existing resumes using Local AI."
    )

    st.subheader("✨ Features")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "📝 Resume Builder\n\n"
            "Create a professional resume using your details."
        )

    with col2:

        st.info(
            "🔍 Resume Analyzer\n\n"
            "Upload your resume and get AI-based analysis."
        )

    with col3:

        st.info(
            "🎯 ATS Analysis\n\n"
            "Get ATS score, keywords and improvement suggestions."
        )

    st.divider()

    st.subheader("🧠 AI Technology")

    st.write(
        "This project uses Ollama with the local Llama 3.2 model. "
        "Your resume information is processed locally."
    )


# ============================================================
# BUILD RESUME
# ============================================================

elif option == "📝 Build Resume":

    st.header("📝 Build Your Resume")

    st.subheader("👤 Personal Information")

    name = st.text_input("Full Name")

    email = st.text_input("Email")

    phone = st.text_input("Phone Number")

    location = st.text_input("Location")

    st.subheader("🎓 Education")

    education = st.text_area(
        "Education",
        placeholder="B.Tech in Data Science..."
    )

    st.subheader("💻 Skills")

    skills = st.text_area(
        "Skills",
        placeholder="Python, SQL, Machine Learning, Java..."
    )

    st.subheader("🚀 Projects")

    projects = st.text_area(
        "Projects",
        placeholder="Project name and description..."
    )

    st.subheader("💼 Experience / Internships")

    experience = st.text_area(
        "Experience",
        placeholder="Internship or work experience..."
    )

    st.subheader("🏆 Certifications")

    certifications = st.text_area(
        "Certifications",
        placeholder="Python Certification..."
    )

    if st.button("🤖 Generate Resume"):

        if name == "":

            st.warning("Please enter your name.")

        else:

            prompt = f"""
You are a professional resume writer.

Create a professional ATS-friendly resume.

Use ONLY the information provided below.
Do not invent any information.

Name:
{name}

Email:
{email}

Phone:
{phone}

Location:
{location}

Education:
{education}

Skills:
{skills}

Projects:
{projects}

Experience / Internships:
{experience}

Certifications:
{certifications}

Create the resume with these sections:

1. Professional Summary
2. Education
3. Skills
4. Projects
5. Experience / Internships
6. Certifications

Use professional wording.
"""

            with st.spinner(
                "Llama 3.2 is creating your resume..."
            ):

                result = ask_llama(prompt)

            st.success("Resume generated successfully!")

            st.subheader("📄 Your AI Generated Resume")

            st.markdown(result)


# ============================================================
# ANALYZE RESUME
# ============================================================

elif option == "🔍 Analyze Resume":

    st.header("🔍 AI Resume Analyzer")

    uploaded_file = st.file_uploader(
        "Upload your resume PDF",
        type=["pdf"]
    )

    job_description = st.text_area(
        "💼 Job Description",
        placeholder="Paste the job description here..."
    )

    if uploaded_file:

        if st.button("🔎 Analyze Resume"):

            with st.spinner("Reading your resume..."):

                resume_text = extract_pdf_text(
                    uploaded_file
                )

            if resume_text.strip() == "":

                st.error(
                    "No text could be extracted from this PDF."
                )

            else:

                st.success(
                    "Resume uploaded successfully!"
                )

                prompt = f"""
You are an expert Resume Analyzer and ATS specialist.

Analyze this resume carefully.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Give the analysis in this format:

# ATS Score

Give an estimated ATS score from 0 to 100.

# Resume Summary

Give a short summary of the candidate.

# Skills Found

List the important skills found.

# Missing Skills

Compare the resume with the job description
and list missing skills.

# ATS Keywords

List important keywords that can improve
the resume for this job.

# Strengths

List the strong points.

# Weaknesses

List the weak points.

# Grammar Suggestions

Suggest improvements to grammar and wording.

# Formatting Suggestions

Give suggestions to improve resume formatting.

# Final Recommendations

Give 5 practical recommendations.

Do not invent information.
"""

                with st.spinner(
                    "Llama 3.2 is analyzing your resume..."
                ):

                    analysis = ask_llama(prompt)

                st.subheader("🤖 AI Resume Analysis")

                st.markdown(analysis)

                with st.expander(
                    "📄 View Extracted Resume Text"
                ):

                    st.write(resume_text)