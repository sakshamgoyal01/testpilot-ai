import streamlit as st
import requests
import os # Import the os module to read environment variables
import json # Import json for potentially structured outputs

st.title("🧪 Run Tests")

# File uploader for test files
uploaded_file = st.file_uploader("📁 Upload Test File", type=["py", "json", "js", "txt"]) # Added 'txt' for broader compatibility

# Dropdown for selecting test type
test_type = st.selectbox("Test Type", ["Unit", "API", "UI"])

# Checkbox for AI-powered error explanation
debug_ai = st.checkbox("🔍 Use AI to explain errors")

# Display file preview if a file is uploaded
if uploaded_file:
    content = uploaded_file.getvalue().decode("utf-8")
    st.text_area("📄 File Preview", content, height=200)

# Button to trigger test execution
if st.button("▶️ Run Test"):
    if uploaded_file is not None:
        st.info("🏃‍♀️ Running tests...")

        # --- Configuration for Backend Connection ---
        # This is crucial for Dockerized environments.
        # It tries to get the backend host from an environment variable (e.g., BACKEND_HOST="testpilot-backend").
        # If the environment variable is not set (e.g., during local development or if running individually),
        # it defaults to "testpilot-backend", which should be your backend Docker service/container name.
        BACKEND_HOST = "testpilot-backend"
        BACKEND_PORT = 8000 # Default to port 8000

        API_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}/api/run-tests" # Backend API endpoint for running tests

        try:
            # Prepare the files part of the request
            # requests expects a tuple: ('filename', file_content, 'content_type')
            # For Streamlit's file_uploader, uploaded_file is a BytesIO-like object,
            # which requests can often handle directly if the method doesn't consume it.
            # However, file.read() is safer to ensure content is passed correctly.
            file_content = uploaded_file.getvalue() # Get byte content
            file_name = uploaded_file.name
            files = {
                "file": (file_name, file_content, "application/octet-stream") # Generic content type
            }

            # Prepare the data part of the request (for form fields)
            # debug_ai needs to be a string ('true' or 'false') for typical web forms/APIs
            data = {
                "type": test_type,
                "debug_with_ai": str(debug_ai).lower()
            }

            st.markdown(f"Attempting to send request to backend at: `{API_URL}`")

            with st.spinner("Executing tests via backend..."):
                # Make the POST request to the backend API
                # Using 'files' for the file upload and 'data' for form fields
                res = requests.post(API_URL, files=files, data=data, timeout=300) # Increased timeout for test execution
                res.raise_for_status() # Raise an HTTPError for bad status codes (4xx or 5xx)

            # If the response is successful (status code 200)
            response_data = res.json()

            st.success("✅ Test execution complete!")

            # Display the test output
            output = response_data.get("output", "No test output provided by backend.")
            st.subheader("📊 Test Output:")
            st.code(output, language="python" if test_type == "Unit" else "text") # Default to text if not unit test

            # Display AI analysis if debug_ai is enabled and analysis is available
            if debug_ai:
                error_ai_analysis = response_data.get("error_ai")
                if error_ai_analysis:
                    st.error("🧠 AI Analysis of Errors:")
                    st.markdown(error_ai_analysis)
                else:
                    st.info("AI debugging was requested, but no 'error_ai' output was provided by the backend.")

        except requests.exceptions.ConnectionError as e:
            # This error occurs if the frontend cannot reach the backend service
            st.error(f"❌ Connection Error: Failed to connect to the backend at `{API_URL}`.")
            st.error(f"Details: {e}")
            st.warning("Please ensure your backend Docker container (`testpilot-backend`) is running and healthy on the same Docker network as this frontend app.")
            st.warning("Verify its logs (`docker logs testpilot-backend`) and ensure it's listening on `0.0.0.0:8000`.")
        except requests.exceptions.Timeout:
            st.error(f"⌛ Request Timeout: The backend at `{API_URL}` did not respond in time.")
            st.info("Test execution might be taking too long, or the backend is overloaded. Consider increasing the timeout or checking backend performance.")
        except requests.exceptions.HTTPError as e:
            # This error occurs if the backend responds with a 4xx or 5xx status code
            st.error(f"❌ Backend Error: The API call failed with status code {e.response.status_code}.")
            st.text(f"Response from backend: {e.response.text}")
            st.info("Check your backend logs for specific error messages (`docker logs testpilot-backend`).")
        except requests.exceptions.RequestException as e:
            # Catch-all for other requests-related errors
            st.error(f"An error occurred while making the request: {e}")
        except json.JSONDecodeError as e:
            # Catches errors if res.json() fails (e.g., if backend sends non-JSON response)
            st.error(f"Error parsing backend response as JSON: {e}")
            if 'res' in locals() and res is not None:
                st.text(f"Raw backend response: {res.text}")
        except Exception as e:
            # General catch-all for any other unexpected errors
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("⚠️ Please upload a test file before running.")

