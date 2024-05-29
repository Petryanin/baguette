"""Reply-разметки клавиатуры."""

from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup

from app.text import buttons


def get_main_kb() -> ReplyKeyboardMarkup:
    """Возвращает основную клавиатуру."""
    button_add = KeyboardButton(text=buttons.ADD)
    button_list = KeyboardButton(text=buttons.LIST)
    return ReplyKeyboardMarkup(
        keyboard=[[button_add, button_list]],
        resize_keyboard=True,
    )


def get_start_kb() -> ReplyKeyboardMarkup:
    """Возвращает стартовую клавиатуру для выбора часового пояса."""
    button_location = KeyboardButton(text=buttons.LOCATION, request_location=True)
    return ReplyKeyboardMarkup(
        keyboard=[[button_location]],
        resize_keyboard=True,
    )
