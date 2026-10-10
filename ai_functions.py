import os
import streamlit as st
from io import BytesIO
from dotenv import load_dotenv
from google import genai
from huggingface_hub import InferenceClient
from PIL import Image
import requests

load_dotenv()

def get_API_Key(name):
    key = os.getenv(name)
    if key:
        return key
    try:
        return st.secrets[name]
    except Exception:
        return None

GEMINI_API_KEY = get_API_Key("GEMINI_API_KEY")
HF_TOKEN = get_API_Key("HF_TOKEN")


def generate_structure(prompt, model, project_type, answer_size, language):
    full_prompt = (f"Створи структуру проєкту. Мова: {language}, ідея: {prompt}, тип проєкту: {project_type}, детальність: {answer_size} включи назву, мету, основні функції, цільову аудиторію, ризики та план розробки в днях. Для короткої відповіді залиш найважливіше, для середньої поясни компоненти, для розгорнутої додай деталі та етапи.")

    try:
        if model == "Gemini":
            if not GEMINI_API_KEY:
                return None, "Не знайдено GEMINI_API_KEY у файлі .env"
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = client.interactions.create(model="gemini-3.8-flash", input=full_prompt)
            return response.output_text, None

        if not HF_TOKEN:
            return None, "Не знайдено HF_TOKEN у файлі .env"
        client = InferenceClient(api_key=HF_TOKEN)
        response = client.chat_completion(
            model="openai/gpt-oss-120b:fastest",
            messages=[
                {"role": "system", "content": "Ти AI Project Architect."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens={"Коротка": 500, "Середня": 1200, "Розгорнута": 2500}[answer_size]
        )
        return response.choices[0].message.content, None
    except Exception as e:
        return None, f"Помилка API: {e}"

import requests  # Убедитесь, что эта строчка есть в самом верху файла!

import requests

def generate_image(prompt, reference_image=None):
    try:
        # Проверяем промпт. Если туда по ошибке передали текст прошлой ошибки или лог,
        # заменяем его на красивый стандартный промпт для вашей тематики.
        if not prompt or "Помилка" in str(prompt) or "HTTP" in str(prompt) or "Client error" in str(prompt):
            prompt = "Modern educational application icon, high quality, 3D render, minimalist vector"

        # Очищаем текст и безопасно кодируем его для интернет-ссылки
        clean_prompt = str(prompt).strip()
        encoded_prompt = requests.utils.quote(clean_prompt)
        
        # Строгий и неизменяемый базовый URL бесплатного сервиса
        base_url = "https://pollinations.ai"
        url = f"{base_url}{encoded_prompt}?width=1024&height=1024&nologo=true"
        
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            return response.content, None
        else:
            return None, f"Помилка сервера генерації: статус {response.status_code}"
            
    except Exception as e:
        return None, f"Помилка генерації зображення: {e}"



def main_ai_function(user_input, model, project_type, answer_size, language):
    return generate_structure(user_input, model, project_type, answer_size, language)


if __name__ == "__main__":
    result, error = main_ai_function("Застосунок для навчання", "Gemini", "Вебзастосунок", "Коротка")
    if error:
        print(f"Помилка: {error}")
    else:
        print(result)