# ✉️ AI Cover Letter Generator

An AI-powered tool that generates tailored, specific cover letters by matching your resume against a job description — instead of generic, templated fluff.

**🔗 Live Demo:** [Add your Streamlit Cloud URL here after deployment]

![Demo](demo.gif)
<!-- Record a short GIF of the upload -> generate -> download flow and add it here -->

---

## 🎯 What it does

1. Upload your resume (PDF) or paste it as text
2. Paste the job description you're applying to
3. Pick a tone (Professional / Enthusiastic / Formal / Conversational)
4. Get a tailored cover letter that highlights the strongest overlaps between your background and the role
5. Edit it inline and download as `.txt`

No generic "I am a hardworking individual" filler — the model is explicitly prompted to reference concrete skills and experience from your resume that match the JD.

---

## 🛠️ Tech Stack

- **Frontend/UI:** Streamlit
- **LLM Orchestration:** LangChain
- **Model:** Qwen/Qwen3-8B (via Hugging Face Inference Endpoint)
- **PDF Parsing:** pypdf
- **Config:** python-dotenv

---

## 📸 Screenshot

<!-- Add a screenshot of the app UI here -->
![App Screenshot](screenshot.png)

---

## 🚀 Running Locally

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up your environment variable**

Copy `.env.example` to `.env` and add your Hugging Face token:
```
HUGGINGFACEHUB_API_TOKEN=your_token_here
```
Get a token from [Hugging Face Settings → Access Tokens](https://huggingface.co/settings/tokens).

**4. Run the app**
```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
├── app.py              # Main Streamlit app
├── requirements.txt     # Python dependencies
├── .env.example         # Sample env file (no real keys)
└── .gitignore
```

---

## 🧠 How it works under the hood

- Resume text is extracted from the uploaded PDF using `pypdf`, or taken directly if pasted
- A single structured prompt (via `ChatPromptTemplate`) feeds the resume, job description, and selected tone to the LLM
- The model is instructed to identify the strongest overlaps between the candidate's background and the role, and write a concise (~350 word) letter reflecting that
- Output is rendered in an editable text area so the user can tweak before downloading

---

## 📌 Future Improvements

- [ ] Split the single prompt into an extract → match → generate chain for higher-quality output
- [ ] Support `.docx` resume uploads
- [ ] Export final letter as a formatted `.docx`
- [ ] Add multiple letter-length options (short/medium/long)

---

## 👤 Author

Built by **Luv Mangla** as part of an AI Engineering learning roadmap (Phase 0 project).
