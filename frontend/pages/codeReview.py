import streamlit as st
import requests
import os # Import the os module to read environment variables

st.title("🔐 AI-Powered Code Review & Risk Scoring")

# File uploader for code files
file = st.file_uploader("Upload code file (.py, .js, .ts)", type=["py", "js", "ts"])
BACKEND_HOST = "testpilot-backend"
BACKEND_PORT = 8000
API_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}/api/code-review"

if file:
    st.info("🧠 Analyzing file for vulnerabilities and bad practices...")


    try:
        # Read the file content and name from the uploaded file object
        file_content = file.read()
        file_name = file.name

        # Prepare the 'files' dictionary for requests.post
        # It expects a tuple: ('filename', file_content, 'content_type')
        files_to_send = {"file": (file_name, file_content, "application/octet-stream")}
        # You might refine 'application/octet-stream' to 'text/x-python', 'application/javascript' etc.
        # based on file type, but 'octet-stream' is a safe default.

        st.markdown(f"Attempting to send request to backend at: `{API_URL}`")

        # Make the POST request to the backend API
        res = requests.post(API_URL, files=files_to_send, timeout=60) # Added a timeout for robustness
        res.raise_for_status() # Raise an HTTPError for bad status codes (4xx or 5xx)

        # If the response is successful (status code 200)
        data = res.json()

        st.success("Analysis complete!")

        # Display Risk Score
        risk_score = data.get("risk_score")
        if risk_score is not None:
            st.subheader("📉 Risk Score")
            # Ensure risk_score is a number for the progress bar
            try:
                numeric_risk_score = float(risk_score)
                st.progress(numeric_risk_score / 100)
                st.write(f"Score: `{numeric_risk_score}`")
            except ValueError:
                st.warning(f"Could not display risk score progress: '{risk_score}' is not a valid number.")
                st.write(f"Score: `{risk_score}`")
        else:
            st.info("No 'risk_score' found in the backend response.")


        # Display Semgrep Output
        semgrep_output = data.get("semgrep_output")
        if semgrep_output:
            st.subheader("🧪 Semgrep Output")
            st.code(semgrep_output[:3000], language="json") # Limiting to 3000 chars for display
            if len(semgrep_output) > 3000:
                st.info("Semgrep output truncated for display purposes.")
        else:
            st.info("No 'semgrep_output' found in the backend response.")


        # Display AI Suggestions
        ai_feedback = data.get("ai_feedback")
        if ai_feedback:
            st.subheader("💡 AI Suggestions")
            st.markdown(ai_feedback)
        else:
            st.info("No 'ai_feedback' found in the backend response.")

    except requests.exceptions.ConnectionError as e:
        # This error occurs if the frontend cannot reach the backend service
        st.error(f"❌ Connection Error: Failed to connect to the backend at `{API_URL}`.")
        st.error(f"Details: {e}")
        st.warning("Please ensure your backend Docker container (`testpilot-backend`) is running and healthy on the same Docker network as this frontend app.")
        st.warning("Verify its logs (`docker logs testpilot-backend`) and ensure it's listening on `0.0.0.0:8000`.")
    except requests.exceptions.Timeout:
        st.error(f"⌛ Request Timeout: The backend at `{API_URL}` did not respond in time.")
        st.info("The backend might be overloaded, or the analysis is taking too long. Try again later.")
    except requests.exceptions.HTTPError as e:
        # This error occurs if the backend responds with a 4xx or 5xx status code
        st.error(f"❌ Backend Error: The API call failed with status code {e.response.status_code}.")
        st.text(f"Response from backend: {e.response.text}")
        st.info("Check your backend logs for specific error messages (`docker logs testpilot-backend`).")
    except requests.exceptions.RequestException as e:
        # Catch-all for other requests-related errors
        st.error(f"An error occurred while making the request: {e}")
    except ValueError as e:
        # Catches errors if res.json() fails (e.g., if backend sends non-JSON response)
        st.error(f"Error parsing backend response as JSON: {e}")
        if res is not None:
            st.text(f"Raw backend response: {res.text}")
    except Exception as e:
        # General catch-all for any other unexpected errors
        st.error(f"An unexpected error occurred: {e}")

