import openai
import secret_data
import asyncio

model = secret_data.model

async def ask_chatgpt(question):
    client = openai.AsyncClient(api_key=secret_data.CHATGPT_API_KEY)

    response = await client.chat.completions.create(
        model=f"{model}",
        messages=[
            {
            "role": "user",
            "content": f"{question}",
            }
        ],
    )

    return response.choices[0].message.content



async def check_chatgpt(question):
    client = openai.AsyncClient(api_key=secret_data.CHATGPT_API_KEY)

    response = await client.chat.completions.create(
        model=f'{model}',
        messages=[
            {
            "role": "developer",
            "content": "Вы - полезный помощник, который проверяет сообщения на наличие грамматических и пунктуационных ошибок."
            "Ваша задача написать есть ли ошибки и пронумеровать все ошибки, если они есть, а также объяснить в чем они заключаются",
            },
            {
            'role': 'user',
            'content': f'{question}',
            }
        ],
    )

    return response.choices[0].message.content