"""Состояния контекста FSM."""

from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class Start(StatesGroup):
    """Состояния при старте бота."""

    timezone = State()


class UserSettings(StatesGroup):
    """Состояния пользовательских настроек."""

    timezone = State()


class Add(StatesGroup):
    """Состояния добавления напоминания."""

    text = State()
