import openai
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def analyze_code_with_ai(code: str) -> str:
    prompt = f"Please review the following code and provide feedback on potential bugs, code style issues, and improvements:\n\n{code}"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300,
        temperature=0.2
    )

    return response.choices[0].text.strip()
