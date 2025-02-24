import asyncio
import aiogram
import aiogram.types
import aiogram.filters
import aiogram.fsm
import aiogram.fsm.context
import aiogram.fsm.state

import chatgpt_api

import kb
import text
import states


router = aiogram.Router()


async def keep_typing(bot: aiogram.Bot, chat_id: int): # function to keep bot typing while waiting for response
    while True:
        await bot.send_chat_action(chat_id=chat_id, action="typing")
        await asyncio.sleep(4)


@router.message(aiogram.filters.command.CommandStart()) # command to start the bot
async def start_command(message: aiogram.types.Message):
    await message.answer(text.greet_user, reply_markup=kb.menu)


@router.message(aiogram.F.text == "Задать вопрос") # command to ask a question
async def ask_question(message: aiogram.types.Message, state: aiogram.fsm.context.FSMContext):
    await state.set_state(states.Form.waiting_for_question)
    await state.update_data(history=[])
    await message.answer(text.ask_question)


@router.message(aiogram.F.text == "Проверить сообщение") # command to ask a question
async def ask_question(message: aiogram.types.Message, state: aiogram.fsm.context.FSMContext):
    await state.set_state(states.Form.waiting_for_message)
    await state.update_data(history=[])
    await message.answer(text.check_message, parse_mode=aiogram.enums.ParseMode.MARKDOWN)


@router.message(states.Form.waiting_for_question) # processing the question and adding it to the history
async def process_question(message: aiogram.types.Message, state: aiogram.fsm.context.FSMContext):
    typing_task = asyncio.create_task(keep_typing(message.bot, message.chat.id))

    data = await state.get_data()
    history = data.get('history', [])

    if len(history) > 0 and message.reply_to_message and message.reply_to_message.text not in history:
        history.append(
            {
            "role": "assistant", 
            "content": message.reply_to_message.text
            }
        )
    else:
        history = []

    history.append(
        {
        "role": "user", 
        "content": message.text
        }
    )

    if len(history) > 10:
        history = history[-10:]

    response = await chatgpt_api.ask_chatgpt(history)

    await state.update_data(history=history)

    await message.reply(response, parse_mode=aiogram.enums.ParseMode.MARKDOWN)

    typing_task.cancel()


@router.message(states.Form.waiting_for_message) # processing the message
async def process_message(message: aiogram.types.Message, state: aiogram.fsm.context.FSMContext):
    typing_task = asyncio.create_task(keep_typing(message.bot, message.chat.id))
    user_message = message.text

    data = await state.get_data()
    history = data.get('history', [])

    if len(history) > 0 and message.reply_to_message and message.reply_to_message.text not in history:
        history.append(
            {
            "role": "assistant", 
            "content": message.reply_to_message.text
            }
        )
    else:
        history = []

    history.append(
        {
        "role": "user", 
        "content": message.text
        }
    )

    if len(history) > 10:
        history = history[-10:]

    response = await chatgpt_api.check_chatgpt(history)

    await state.update_data(history=history)
    
    await message.reply(response, parse_mode=aiogram.enums.ParseMode.MARKDOWN)

    typing_task.cancel()
