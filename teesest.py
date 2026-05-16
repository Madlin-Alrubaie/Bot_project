import requests
import json

API_KEY = "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"

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model":"openai/gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": "مرحبا"
        }
    ]
}

response = requests.post(
    url,
    headers=headers,
    json=data
)

print(response.status_code)
print(response.text)
