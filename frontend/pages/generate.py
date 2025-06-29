import streamlit as st
import requests
import os # Import the os module to read environment variables
import json # Import json for potentially structured outputs

st.title("🧠 AI Test Case Generator") # Updated title

# File uploader for code, OpenAPI spec, or user stories
file = st.file_uploader("📁 Upload your code, OpenAPI spec or user story", type=["py", "json", "yaml", "txt"])

# Radio buttons for selecting test type
option = st.radio("Generate Test Type", ["Unit Tests", "API Tests", "UI Tests (Playwright)"])
BACKEND_HOST = "testpilot-backend"
BACKEND_PORT = 8000 # Default to port 8000

API_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}/api/gen-tests"

if st.button("🚀 Generate Tests"):
    if file is not None:
        st.info(f"✨ Preparing to generate {option}...")

        try:
            # Read the file content
            content = file.getvalue().decode("utf-8") # .getvalue() is for BytesIO object from file_uploader

            # Prepare the payload for the backend
            payload = {
                "input_text": content,
                "type": option # Pass the selected test type
            }

            st.markdown(f"Attempting to send request to backend at: `{API_URL}`")

            with st.spinner("Generating via AI..."): # Spinner while waiting for response
                # Make the POST request to the backend API
                # Note: 'json' parameter is used for sending JSON payload, not 'files'
                res = requests.post(API_URL, json=payload, timeout=120) # Increased timeout for generation tasks
                res.raise_for_status() # Raise an HTTPError for bad status codes (4xx or 5xx)

            # If the response is successful (status code 200)
            result = res.json()

            st.success("✅ Test case generated!")

            # Display the generated output
            generated_output = result.get("output", "No output generated.")
            output_language = 'python' if 'Unit' in option else 'json' # Default language for code display
            filename_suggestion = result.get("filename", "generated_test_file.txt")

            st.subheader(f"{option} Output:")
            st.code(generated_output, language=output_language)

            # Add download button
            st.download_button(
                label="⬇️ Download Test File",
                data=generated_output,
                file_name=filename_suggestion,
                mime="text/plain" # Adjust MIME type if known (e.g., 'application/json', 'text/x-python')
            )

        except requests.exceptions.ConnectionError as e:
            st.error(f"❌ Connection Error: Failed to connect to the backend at `{API_URL}`.")
            st.error(f"Details: {e}")
            st.warning("Please ensure your backend Docker container (`testpilot-backend`) is running and healthy on the same Docker network as this frontend app.")
            st.warning("Verify its logs (`docker logs testpilot-backend`) and ensure it's listening on `0.0.0.0:8000`.")
        except requests.exceptions.Timeout:
            st.error(f"⌛ Request Timeout: The backend at `{API_URL}` did not respond in time.")
            st.info("The generation task might be taking too long, or the backend is overloaded. Consider increasing the timeout or checking backend performance.")
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
            if 'res' in locals() and res is not None: # Check if 'res' exists and is not None
                st.text(f"Raw backend response: {res.text}")
        except Exception as e:
            # General catch-all for any other unexpected errors
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please upload a file before generating tests.")
