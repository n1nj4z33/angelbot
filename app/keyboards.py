from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

language_selection_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="language_ru")],
        [InlineKeyboardButton(text="🇺🇸 English", callback_data="language_en")],
    ]
)

survey_keyboard_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⚕️ Общие сведения", 
                web_app=WebAppInfo(url="https://n1nj4z33.github.io/angelbot/general_info_ru.html")
            )
        ],
        [
            InlineKeyboardButton(text="🍔 Питание", callback_data="nutrition"),
            InlineKeyboardButton(text="💊 Симптоматика", callback_data="symptoms")],
        [
            InlineKeyboardButton(text="🧠 Нейромедиаторы", callback_data="neurotransmitters"),
            InlineKeyboardButton(text="🫁 ЖДА", callback_data="zhda")],
        [
            InlineKeyboardButton(text="🫀 Надпочечники", callback_data="adrenal_glands"),
            InlineKeyboardButton(text="🌡️ ЖКТ", callback_data="gastrointestinal_tract")
        ],
    ]
)

survey_keyboard_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⚕️ General Information",
                web_app=WebAppInfo(url="https://n1nj4z33.github.io/angelbot/genenal_info_en.html")
            )
        ],
        [
            InlineKeyboardButton(text="🍔 Nutrition", callback_data="nutrition"),
            InlineKeyboardButton(text="💊 Symptoms", callback_data="symptoms")
        ],
        [
            InlineKeyboardButton(text="🧠 Neurotransmitters", callback_data="neurotransmitters"),
            InlineKeyboardButton(text="🫁 IDA", callback_data="zhda")
        ],
        [
            InlineKeyboardButton(text="🫀 Adrenal Glands", callback_data="adrenal_glands"), 
            InlineKeyboardButton(text="🌡️ Gastrointestinal Tract", callback_data="gastrointestinal_tract")
        ]
    ]
)


gastrointestinal_tract_keyboard_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Нет или редко", callback_data="0")],
        [InlineKeyboardButton(text="Иногда", callback_data="1")],
        [InlineKeyboardButton(text="Часто", callback_data="4")],
        [InlineKeyboardButton(text="Очень часто", callback_data="8")],
    ]
)

gastrointestinal_tract_keyboard_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="No or Rarely", callback_data="0")],
        [InlineKeyboardButton(text="Sometimes", callback_data="1")],
        [InlineKeyboardButton(text="Often", callback_data="4")],
        [InlineKeyboardButton(text="Very Often", callback_data="8")],
    ]
)


# New keyboards for the adrenal glands survey
adrenal_glands_keyboard_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Нет или редко", callback_data="0")],
        [InlineKeyboardButton(text="Иногда", callback_data="1")],
        [InlineKeyboardButton(text="Часто", callback_data="4")],
        [InlineKeyboardButton(text="Очень часто", callback_data="8")],
    ]
)

adrenal_glands_keyboard_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="No or Rarely", callback_data="0")],
        [InlineKeyboardButton(text="Sometimes", callback_data="1")],
        [InlineKeyboardButton(text="Often", callback_data="4")],
        [InlineKeyboardButton(text="Very Often", callback_data="8")],
    ]
)