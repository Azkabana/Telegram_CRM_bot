from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

ask_text = input("Введите текст: ")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=ask_text,
)

print(response.text)

# рабочий шаблон
# НЕ влияет на общий шаблон
