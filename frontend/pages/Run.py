import streamlit as st
import requests

st.title("🧪 Run Tests")

uploaded_file = st.file_uploader("📁 Upload Test File", type=["py", "json", "js"])
test_type = st.selectbox("Test Type", ["Unit", "API", "UI"])
debug_ai = st.checkbox("🔍 Use AI to explain errors")

if uploaded_file:
    content = uploaded_file.getvalue().decode("utf-8")
    st.text_area("📄 File Preview", content, height=200)

if st.button("▶️ Run Test"):
    if uploaded_file is not None:
        with st.spinner("Running tests..."):
            files = {
                "file": (uploaded_file.name, uploaded_file, "multipart/form-data")
            }
            data = {
                "type": test_type,
                "debug_with_ai": str(debug_ai).lower()  # ✅ required
            }

            res = requests.post("http://localhost:8000/api/run-tests", files=files, data=data)

            if res.ok:
                data = res.json()
                st.code(data["output"], language="python")

                if debug_ai and data.get("error_ai"):
                    st.error("🧠 AI Analysis:")
                    st.write(data["error_ai"])
            else:
                st.error(f"❌ Test failed to run. {res.text}")
    else:
        st.warning("⚠️ Please upload a test file before running.")
