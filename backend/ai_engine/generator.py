import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)


def build_prompt(input_text: str, type_: str) -> tuple:
    system_prompt = "You are an AI that generates high-quality test cases."

    if "Unit" in type_:
        user_prompt = f"Generate PyTest test cases for the following Python code:\n\n{input_text}"
    elif "API" in type_:
        user_prompt = f"Generate Postman-compatible API tests from this OpenAPI/Swagger spec:\n\n{input_text}"
    elif "UI" in type_:
        user_prompt = f"Generate Playwright-based frontend tests from this user story:\n\n{input_text}"
    else:
        user_prompt = f"Generate test cases for:\n\n{input_text}"

    user_prompt += "\n\nAdd test metadata like @critical, @regression, @smoke where relevant."

    return system_prompt, user_prompt


def generate_tests_with_type(input_text: str, type_: str):
    system_prompt, user_prompt = build_prompt(input_text, type_)

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # or mixtral-8x7b-32768
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        output = response.choices[0].message.content.strip()
        ext = "py" if "Unit" in type_ else "json" if "API" in type_ else "js"
        filename = f"generated_test.{ext}"
        return output, filename

    except Exception as e:
        print("🔥 Groq/OpenAI API error:", str(e))
        return f"Error: {str(e)}", "error.log"
