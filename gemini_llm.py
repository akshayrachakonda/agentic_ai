import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def call_llm(prompt: str, temperature: float = 0) -> str:
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": temperature
        }
    )
    return response.text.strip()
