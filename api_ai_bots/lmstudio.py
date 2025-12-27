from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
URL_LMS = os.getenv("URL_LMS")


# Настройка клиента на локальный адрес LM Studio
async def ai_gen_usertext(user_text):
    print("start ai_gen_usertext: True")
    client = OpenAI(base_url=URL_LMS, api_key="none")
    response = client.chat.completions.create(
        model="meta-llama-3.1-8b-instruct",
        messages=[
            {
                "role": "system",
                "content": """Ты — оператор поддержки салона красоты.
                Отвечай строго и кратко, простым языком. 
                Ответ — 1–2 предложения.Не используй технические термины.
                Не задавай вопросов, не связанных с записью. 
                Не начинай новое предложение, если нехватает тикетов его закончить.
                Ниже переписка с клиентом {user_text}
                Твоя задача — сформировать следующий ответ оператору, который можно отправить клиенту
                """,
            },
            {"role": "user", "content": user_text},
        ],
        max_tokens=50,
    )
    gen_usertext = response.choices[0].message.content
    print("text genereted: True")
    return gen_usertext
