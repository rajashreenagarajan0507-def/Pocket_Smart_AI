import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_recommendation(prompt: str) -> str:
    if not GEMINI_API_KEY:
        return "Gemini API key is not configured."

    try:
        response = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        return f"Gemini error: {str(e)}"
