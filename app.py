import streamlit as st
from groq import Groq
from pypdf import PdfReader

# -----------------------
# Enter your Groq API Key
# -----------------------
GROQ_API_KEY = "YOUR_GROQ_API_KEY"

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="AI Medical Report Explainer", page_icon="🏥")

st.title("🏥 AI Medical Report Explainer")
st.write("Upload a medical report (PDF) and get an easy-to-understand AI explanation.")

uploaded_file = st.file_uploader(
    "Upload Medical Report (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:

    reader = PdfReader(uploaded_file)

    report_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            report_text += text

    st.success("✅ Medical report uploaded successfully!")

    if st.button("Analyze Report"):

        with st.spinner("Analyzing..."):

            prompt = f"""
You are a helpful medical AI assistant.

Read the following medical report and explain it in very simple English.

Provide:

1. Summary
2. Important Findings
3. Health Precautions
4. Lifestyle Suggestions
5. When the patient should consult a doctor

Do NOT give a final diagnosis.
Mention that this is only an AI-generated explanation.

Medical Report:

{report_text}
"""

            try:

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": "You explain medical reports in simple language."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                st.subheader("🤖 AI Explanation")
                st.write(response.choices[0].message.content)

                st.warning(
                    "⚠️ This explanation is AI-generated and should not replace professional medical advice."
                )

            except Exception as e:
                st.error(f"Error: {e}")