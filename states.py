import aiogram.fsm.state


class Form(aiogram.fsm.state.StatesGroup):
    waiting_for_question = aiogram.fsm.state.State()
    processing_question = aiogram.fsm.state.State()
