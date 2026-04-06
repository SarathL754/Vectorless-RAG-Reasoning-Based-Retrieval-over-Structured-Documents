import os
from dotenv import load_dotenv
import openai

load_dotenv()


async def call_llm(prompt, model="gpt-5.4-nano",temperature=0):
    client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content.strip()