# app/states.py
from aiogram.fsm.state import State, StatesGroup


class SurveyStates(StatesGroup):
    waiting_for_answer = State()
    editing_answer = State()
    survey_type = State()
