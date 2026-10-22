import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

try:
    client = genai.Client()
    print("Available Models:")
    for model in client.models.list():
        print(model.name)
except Exception as e:
    print("Error:", e)