"""
AI Cover Letter Generator
--------------------------
Full Stack AI Engineer path

Flow: Resume (PDF/text) + Job Description -> LLM extraction -> matching -> generation -> editable output
"""
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
import os
import streamlit as st
from pypdf import PdfReader
from langchain_core.prompts import ChatPromptTemplate


# ---------------------------------------------------------
# PAGE CONFIG (must be the first Streamlit command in the script)
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Cover Letter Generator",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()

# ---------------------------------------------------------
# LLM SETUP (cached so it only initializes once, not on every rerun)
# ---------------------------------------------------------
@st.cache_resource
def load_model():
    llm = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen3-8B",
        task="text-generation",
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
        max_new_tokens=1024,
        temperature=0.7,
    )
    return ChatHuggingFace(llm=llm)

model = load_model()

# ---------------------------------------------------------
# SESSION STATE INIT
# ---------------------------------------------------------
# Streamlit reruns the whole script on every interaction,
# so anything that needs to persist across reruns lives here.
defaults = {
    "resume_text": "",
    "jd_text": "",
    "generated_letter": "",
    "matching_points": None,
    "tone": "Professional",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------
def extract_pdf_text(uploaded_file) -> str:
    """Extract raw text from an uploaded PDF file object."""
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    return text.strip()


def generate_cover_letter(resume_text: str, jd_text: str, tone: str) -> str:
    """
    Calls the LLM to generate a tailored cover letter.
    (Simple single-prompt version for now — can be split into
    extract -> match -> generate chain later for better quality.)
    """
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert career coach who writes tailored, specific, "
            "non-generic cover letters. Avoid clichés like 'hardworking individual'. "
            "Reference concrete skills/experience from the resume that match the job description.",
        ),
        (
            "human",
            "Resume:\n{resume}\n\n"
            "Job Description:\n{jd}\n\n"
            "Write a {tone} cover letter (max 350 words) tailored to this job, "
            "highlighting the strongest overlaps between the resume and the JD.",
        ),
    ])

    chain = prompt | model
    response = chain.invoke({"resume": resume_text, "jd": jd_text, "tone": tone.lower()})
    return response.content


# ---------------------------------------------------------
# SIDEBAR — Settings / Controls
# ---------------------------------------------------------
with st.sidebar:
    st.header("Settings")

    st.session_state.tone = st.selectbox(
        "Tone",
        ["Professional", "Enthusiastic", "Formal", "Conversational"],
        index=["Professional", "Enthusiastic", "Formal", "Conversational"].index(
            st.session_state.tone
        ),
    )

    st.divider()
    st.caption("AI-powered Cover Letter Generator")
    st.caption("Built with Streamlit + LangChain")

    st.divider()
    with st.expander("How it works"):
        st.write(
            "1. Upload or paste your resume\n"
            "2. Paste the job description\n"
            "3. Click Generate\n"
            "4. Edit and download your letter"
        )


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("AI Cover Letter Generator")
st.caption("Turn your resume + a job description into a tailored cover letter in seconds.")
st.divider()


# ---------------------------------------------------------
# MAIN LAYOUT — Two columns: Inputs | Output
# ---------------------------------------------------------
left_col, right_col = st.columns([1, 1], gap="large")

# -------------------- LEFT: INPUTS --------------------
with left_col:
    st.subheader("Your Resume")

    resume_tab1, resume_tab2 = st.tabs(["Upload PDF", "Paste Text"])

    with resume_tab1:
        uploaded_resume = st.file_uploader(
            "Upload your resume (PDF)", type=["pdf"], key="resume_upload"
        )
        if uploaded_resume is not None:
            with st.spinner("Extracting text from PDF..."):
                extracted = extract_pdf_text(uploaded_resume)
                st.session_state.resume_text = extracted
            st.success("Resume text extracted")
            with st.expander("Preview extracted text"):
                st.text_area(
                    "Extracted content",
                    st.session_state.resume_text,
                    height=200,
                    label_visibility="collapsed",
                )

    with resume_tab2:
        pasted_resume = st.text_area(
            "Paste your resume text",
            value=st.session_state.resume_text,
            height=250,
            placeholder="Paste your resume content here...",
        )
        if pasted_resume:
            st.session_state.resume_text = pasted_resume

    st.subheader("Job Description")
    jd_input = st.text_area(
        "Paste the job description",
        value=st.session_state.jd_text,
        height=250,
        placeholder="Paste the JD you're applying to...",
    )
    if jd_input:
        st.session_state.jd_text = jd_input

    st.write("")  # spacing
    generate_clicked = st.button(
        "Generate Cover Letter", type="primary", use_container_width=True
    )

# -------------------- RIGHT: OUTPUT --------------------
with right_col:
    st.subheader("Your Cover Letter")

    if generate_clicked:
        if not st.session_state.resume_text.strip():
            st.warning("Please upload or paste your resume first.")
        elif not st.session_state.jd_text.strip():
            st.warning("Please paste the job description first.")
        else:
            with st.spinner("Analyzing your fit and drafting the letter..."):
                letter = generate_cover_letter(
                    st.session_state.resume_text,
                    st.session_state.jd_text,
                    st.session_state.tone,
                )
                st.session_state.generated_letter = letter

    if st.session_state.generated_letter:
        edited_letter = st.text_area(
            "Editable output",
            value=st.session_state.generated_letter,
            height=400,
            label_visibility="collapsed",
        )
        st.session_state.generated_letter = edited_letter

        dl_col1, dl_col2 = st.columns(2)
        with dl_col1:
            st.download_button(
                "Download as .txt",
                data=st.session_state.generated_letter,
                file_name="cover_letter.txt",
                use_container_width=True,
            )
        with dl_col2:
            st.button("Regenerate", use_container_width=True)
    else:
        st.info("Your generated cover letter will appear here once you click Generate.")


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.divider()
st.caption("Built by Luv Mangla")