import streamlit as st
import requests

st.title("🔐 AI-Powered Code Review & Risk Scoring")

file = st.file_uploader("Upload code file (.py, .js, .ts)", type=["py", "js", "ts"])

if file:
    st.info("🧠 Analyzing file for vulnerabilities and bad practices...")
    res = requests.post("http://localhost:8000/api/code-review", files={"file": file})

    if res.ok:
        data = res.json()
        st.subheader("📉 Risk Score")
        st.progress(data["risk_score"] / 100)
        st.write(f"Score: `{data['risk_score']}`")

        st.subheader("🧪 Semgrep Output")
        st.code(data["semgrep_output"][:3000], language="json")

        st.subheader("💡 AI Suggestions")
        st.markdown(data["ai_feedback"])
    else:
        st.error("Review failed.")
