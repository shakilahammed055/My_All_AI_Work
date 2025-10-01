import requests
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
print("=====", os.getenv("OPENROUTER_API_KEY"))


def chatboat(prompt):

    completion = client.chat.completions.create(
        extra_body={},
        model="x-ai/grok-4-fast:free",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
                        },
                    },
                ],
            }
        ],
    )
    print(completion)
    msg=completion.choices[0].message.content
    return msg


if __name__ == "__main__":
    msg = chatboat("Hello, how are you?")
    print(msg)
