import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq-compatible OpenAI client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")  # Use GROQ key here
)

def analyze_error(error_log: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # or "mixtral-8x7b-32768"
            messages=[
                {"role": "system", "content": "You're an expert at analyzing test failures."},
                {"role": "user", "content": f"Explain the following test failure log:\n\n{error_log}"}
            ],
            temperature=0.3,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Error while calling Groq API: {str(e)}"
