import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

hindsight_key = os.getenv("HINDSIGHT_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

print("Checking environment variables...")

if hindsight_key:
    print("✅ Hindsight API key found")
else:
    print("❌ Hindsight API key missing")

if groq_key:
    print("✅ Groq API key found")
else:
    print("❌ Groq API key missing")

if groq_key:
    try:
        client = Groq(api_key=groq_key)

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": "Reply with exactly: Groq connection successful"
                }
            ],
            max_tokens=50
        )

        print("\n🤖 Groq response:")
        print(response.choices[0].message.content)

    except Exception as e:
        print("\n❌ Groq connection failed:")
        print(e)