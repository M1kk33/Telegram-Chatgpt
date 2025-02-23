import aiogram.types

menu=aiogram.types.ReplyKeyboardMarkup(
    keyboard=[
        [
            aiogram.types.KeyboardButton(text="Задать вопрос"),
            aiogram.types.KeyboardButton(text="Проверить сообщение"),
        ]
    ],
    resize_keyboard=True,
)
