import openai, os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq-compatible client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_ai_for_review(code_path: str) -> str:
    # Read the source code file
    with open(code_path, "r") as file:
        code = file.read()

    # Prompt to the LLM
    prompt = f"""
You are a secure code reviewer. Analyze the following code and:

1. Identify vulnerabilities, code smells, bad practices
2. Give suggestions to improve them
3. Provide a risk score (0–100) if possible

Code:
{code}
"""

    try:
        # Use Groq-compatible client (e.g., LLaMA3 or Mixtral)
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # or "mixtral-8x7b-32768"
            messages=[
                {"role": "system", "content": "You are a senior secure code auditor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Error: {str(e)}"
