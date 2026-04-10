import os
import requests

API_KEY = os.getenv("API_KEY")

def call_qwen(user_input):
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "qwen-turbo",
        "input": {
            "prompt": user_input
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["output"]["text"]
