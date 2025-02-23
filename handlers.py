import asyncio
import aiogram
import aiogram.types
import aiogram.filters
import aiogram.fsm
import aiogram.fsm.context
import aiogram.fsm.state


import kb
import text
import states

import chatgpt_api


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
    await message.answer(text.ask_question)


@router.message(states.Form.waiting_for_question) # processing the question
async def process_question(message: aiogram.types.Message, state: aiogram.fsm.context.FSMContext):
    user_question = message.text

    typing_task = asyncio.create_task(keep_typing(message.bot, message.chat.id))

    try:
        response = await chatgpt_api.ask_chatgpt(user_question)
    finally:
        typing_task.cancel()

    typing_task.cancel()
    
    await message.reply(response)
    await state.clear()


