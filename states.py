import aiogram.fsm.state


class Form(aiogram.fsm.state.StatesGroup):
    waiting_for_question = aiogram.fsm.state.State()
    processing_question = aiogram.fsm.state.State()
    waiting_for_message = aiogram.fsm.state.State()
    processing_message = aiogram.fsm.state.State()
