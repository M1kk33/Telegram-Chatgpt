import openai
import secret_data
import asyncio

model = secret_data.model

async def ask_chatgpt(question):
    client = openai.AsyncClient(api_key=secret_data.CHATGPT_API_KEY)

    response = await client.chat.completions.create(
        model=f'{model}',
        messages=[{
            'role': 'user',
            'content': f'{question}',
        }],
    )

    return response.choices[0].message.content