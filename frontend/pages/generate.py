import streamlit as st
import requests
import json

st.title("🧠 AI Test Case Generator")

file = st.file_uploader("📁 Upload your code, OpenAPI spec or user story", type=["py", "json", "yaml", "txt"])

option = st.radio("Generate Test Type", ["Unit Tests", "API Tests", "UI Tests (Playwright)"])

if st.button("🚀 Generate Tests"):
    if file is not None:
        content = file.getvalue().decode("utf-8")
        payload = {
            "input_text": content,
            "type": option
        }
        with st.spinner("Generating via GPT..."):
            res = requests.post("http://localhost:8000/api/gen-tests", json=payload)
            if res.ok:
                result = res.json()
                st.success("✅ Test case generated!")
                st.code(result['output'], language='python' if 'Unit' in option else 'json')
                st.download_button("⬇️ Download Test File", result['output'], file_name=result['filename'])
            else:
                st.error(f"❌ Failed to generate.\n{res.text}")
