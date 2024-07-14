import requests

url = "https://chatgpt-42.p.rapidapi.com/gpt4"

payload = {
    "messages": [
        {
            "role": "user",
            "content": "hi"
        }
    ],
    "web_access": False
}
headers = {
    "x-rapidapi-key": "9be757d24fmsh8dcd3fa0fbcc651p1ac673jsn65b993d5891a",
    "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())
