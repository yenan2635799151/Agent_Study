from openai import OpenAI

client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key="sk-d1c62c6f9e1546a29f515b631e4f862c"
)

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role":"user","content":"你好"}
    ]
)

print(resp)