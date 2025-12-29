
"""import base64
def ollama_generate(promt, model="gpt-oss:120b-cloud",max_tokens=512):
    import requests
    url = f"http://localhost:11434/api/generate"
    key = "6d09f76b283a434cb125c379d25340bf.vDFVFxhCZiq4NMFYQjtUYGs9"
    data = {
        "model": model,
        "prompt": promt,
        "max_tokens": max_tokens,
        "stream": False}
    response = requests.post(url, json=data)
    return response.json().get("response", "")
print(ollama_generate("how do assign value in a variable in python?"))"""
import base64
from ollama import chat
def ollama_generate(promt, model="qwen3-vl:235b-cloud",max_tokens=512):
    '''with open(r"K:\Code\Project\Advanced_intelligent assistant\A_I_S_H_A\test2.jpg", "rb") as image_file:
        img = base64.b64encode(image_file.read()).decode()'''
    stream = chat(
        model=model,
        messages=[
            {"role": "user",
            "content": promt,
            "images": [r"K:\Code\Project\Advanced_intelligent assistant\A_I_S_H_A\test2.jpg"]
            }
        ],
        stream=True
    )
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
ollama_generate("explain this image")