# app/keyboards.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

language_selection_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Русский", callback_data="language_ru")],
        [InlineKeyboardButton(text="English", callback_data="language_en")],
    ]
)

survey_keyboard_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Общие сведения", callback_data="general_info")],
        [InlineKeyboardButton(text="Питание", callback_data="nutrition")],
        [InlineKeyboardButton(text="Симптоматика", callback_data="symptoms")],
        [InlineKeyboardButton(text="Нейромедиаторы", callback_data="neurotransmitters")],
        [InlineKeyboardButton(text="ЖДА", callback_data="zhda")],
        [InlineKeyboardButton(text="Надпочечники", callback_data="adrenal_glands")],
        [InlineKeyboardButton(text="ЖКТ", callback_data="gastrointestinal_tract")],
    ]
)

survey_keyboard_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="General Information", callback_data="general_info")],
        [InlineKeyboardButton(text="Nutrition", callback_data="nutrition")],
        [InlineKeyboardButton(text="Symptoms", callback_data="symptoms")],
        [InlineKeyboardButton(text="Neurotransmitters", callback_data="neurotransmitters")],
        [InlineKeyboardButton(text="IDA", callback_data="zhda")],
        [InlineKeyboardButton(text="Adrenal Glands", callback_data="adrenal_glands")],
        [
            InlineKeyboardButton(
                text="Gastrointestinal Tract", callback_data="gastrointestinal_tract"
            )
        ],
    ]
)
