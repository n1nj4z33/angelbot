import json

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

import app.keyboards as kb
from app.states import SurveyStates

import os

router = Router()

surveys = {
    "general_info": {"ru": "data/general_info_ru.json", "en": "data/general_info_en.json"},
    "nutrition": {"ru": "data/nutrition_ru.json", "en": "data/nutrition_en.json"},
    "symptoms": {"ru": "data/symptoms_ru.json", "en": "data/symptoms_en.json"},
    "neurotransmitters": {
        "ru": "data/neurotransmitters_ru.json",
        "en": "data/neurotransmitters_en.json",
    },
    "zhda": {"ru": "data/zhda_ru.json", "en": "data/zhda_en.json"},
    "adrenal_glands": {"ru": "data/adrenal_glands_ru.json", "en": "data/adrenal_glands_en.json"},
    "gastrointestinal_tract": {
        "ru": "data/gastrointestinal_tract_ru.json",
        "en": "data/gastrointestinal_tract_en.json",
    },
}

questions_data = {"ru": {}, "en": {}}

for survey, files in surveys.items():
    for lang, filename in files.items():
        try:
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if content:
                    questions_data[lang][survey] = json.loads(content)
                else:
                    print(f"Warning: {filename} is empty.")
                    questions_data[lang][survey] = []
        except json.JSONDecodeError as e:
            print(f"Error loading {filename}: {e}")
            questions_data[lang][survey] = []


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Выберите язык / Choose a language:", reply_markup=kb.language_selection_keyboard
    )


@router.callback_query(F.data == "language_ru")
async def select_language_ru(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(language="ru")
    await callback_query.answer("Язык выбран: Русский")
    await callback_query.message.answer(
        "Добро пожаловать! Выберите опрос:", reply_markup=kb.survey_keyboard_ru
    )


@router.callback_query(F.data == "language_en")
async def select_language_en(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(language="en")
    await callback_query.answer("Language selected: English")
    await callback_query.message.answer(
        "Welcome! Please choose a survey:", reply_markup=kb.survey_keyboard_en
    )


@router.callback_query(lambda call: call.data in surveys)
async def process_survey_callback(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    survey_type = callback_query.data
    language = data.get("language", "ru")
    await state.set_state(SurveyStates.waiting_for_answer)
    await state.update_data(user_responses=[], survey_type=survey_type, language=language)
    await callback_query.answer()
    await callback_query.message.answer(
        "Начнем опрос. Отвечайте на следующие вопросы:"
        if language == "ru"
        else "Let's start the survey. Please answer the following questions:"
    )
    await send_next_question(callback_query.message, state)


async def send_next_question(message: Message, state: FSMContext):
    data = await state.get_data()
    user_responses = data.get("user_responses", [])
    survey_type = data.get("survey_type")
    language = data.get("language", "ru")

    current_question = len(user_responses)

    if current_question < len(questions_data[language][survey_type]):
        await message.answer(questions_data[language][survey_type][current_question])
    else:
        await send_summary(message, state)


@router.message(SurveyStates.waiting_for_answer)
async def handle_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    user_responses = data.get("user_responses", [])
    survey_type = data.get("survey_type")
    language = data.get("language", "ru")
    user_response = message.text

    if len(user_responses) < len(questions_data[language][survey_type]):
        user_responses.append(
            {
                "question": questions_data[language][survey_type][len(user_responses)],
                "answer": user_response,
            }
        )
        await state.update_data(user_responses=user_responses)
        await send_next_question(message, state)
    else:
        await send_summary(message, state)


async def send_summary(message: Message, state: FSMContext):
    data = await state.get_data()
    user_responses = data.get("user_responses", [])
    # survey_type = data.get("survey_type")
    language = data.get("language", "ru")

    if user_responses:
        summary = "Ваши ответы:\n\n" if language == "ru" else "Your responses:\n\n"

        for i, response in enumerate(user_responses):
            summary += (
                f"{i+1}. {response['question']}\nОтвет: {response['answer']}\n\n"
                if language == "ru"
                else f"{i+1}. {response['question']}\nAnswer: {response['answer']}\n\n"
            )

        save_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📝 Редактировать ответы" if language == "ru" else "Edit Responses",
                        callback_data="edit_responses",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="✅ Переслать результаты" if language == "ru" else "Forward Results",
                        callback_data="forward_results",
                    )
                ],
            ]
        )

        await message.answer(summary, reply_markup=save_button)

    else:
        await message.answer(
            "Не удалось найти ваши ответы."
            if language == "ru"
            else "Could not find your responses."
        )


@router.callback_query(F.data == "edit_responses")
async def edit_responses(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(SurveyStates.editing_answer)
    data = await state.get_data()
    language = data.get("language", "ru")
    await callback_query.answer(
        "Выберите вопрос для редактирования:" if language == "ru" else "Select a question to edit:"
    )
    await list_questions(callback_query.message, state)


async def list_questions(message: Message, state: FSMContext):
    data = await state.get_data()
    user_responses = data.get("user_responses", [])
    language = data.get("language", "ru")

    if user_responses:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        for i, response in enumerate(user_responses):
            keyboard.inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        text=f"{i+1}. {response['question']}", callback_data=f"edit_{i}"
                    )
                ]
            )
        await message.answer(
            (
                "Выберите вопрос для редактирования:"
                if language == "ru"
                else "Select a question to edit:"
            ),
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            "Нет ответов для редактирования." if language == "ru" else "No responses to edit."
        )


@router.callback_query(F.data.startswith("edit_"))
async def process_edit_question(callback_query: CallbackQuery, state: FSMContext):
    question_index = int(callback_query.data.split("_")[1])
    await state.update_data(editing_index=question_index)
    data = await state.get_data()
    question = data["user_responses"][question_index]["question"]
    language = data.get("language", "ru")
    await callback_query.message.answer(
        f"Редактирование вопроса: {question}\nВведите новый ответ:"
        if language == "ru"
        else f"Editing question: {question}\nEnter a new answer:"
    )
    await callback_query.answer()


@router.message(SurveyStates.editing_answer)
async def handle_edit_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    editing_index = data.get("editing_index")
    user_responses = data.get("user_responses", [])
    language = data.get("language", "ru")

    if editing_index is not None and 0 <= editing_index < len(user_responses):
        user_responses[editing_index]["answer"] = message.text
        await state.update_data(user_responses=user_responses)
        await state.set_state(SurveyStates.waiting_for_answer)
        await message.answer("Ответ обновлен." if language == "ru" else "Answer updated.")
        await send_summary(message, state)
    else:
        await message.answer(
            "Ошибка при обновлении ответа." if language == "ru" else "Error updating the answer."
        )


@router.callback_query(F.data == "forward_results")
async def forward_results(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_responses = data.get("user_responses", [])
    user_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name}"
    group_chat_id = os.getenv("GROUP_CHAT_ID")
    message_thread_id = os.getenv("MESSAGE_THREAD_ID")
    language = data.get("language", "ru")

    if user_responses:
        summary = "Ваши ответы:\n\n" if language == "ru" else "Your responses:\n\n"

        for i, response in enumerate(user_responses):
            summary += (
                f"{i+1}. {response['question']}\nОтвет: {response['answer']}\n\n"
                if language == "ru"
                else f"{i+1}. {response['question']}\nAnswer: {response['answer']}\n\n"
            )

        await callback_query.message.bot.send_message(
            chat_id=group_chat_id,
            text=(
                f"Результаты от {user_name}:\n\n{summary}"
                if language == "ru"
                else f"Results from {user_name}:\n\n{summary}"
            ),
            message_thread_id=message_thread_id,
        )
        await callback_query.answer(
            "Результаты пересланы!" if language == "ru" else "Results forwarded!"
        )
    else:
        await callback_query.answer(
            "Не удалось переслать результаты."
            if language == "ru"
            else "Could not forward the results."
        )
