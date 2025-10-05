import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def chatboat(prompt):
    completion = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[{"role": "user", "content": prompt}],
    )
    msg = completion.choices[0].message.content
    return msg


if __name__ == "__main__":
    msg = chatboat("Hello, how are you?")
    print(msg)
