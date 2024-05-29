"""Обработчик команды `/help`."""

from aiogram import Router
from aiogram import types
from aiogram.filters import Command

from app.text import messages


router = Router()


@router.message(Command("help"))
async def handle_help_command(message: types.Message) -> None:
    """Обработчик команды `/help`.

    Args:
        message: Объект сообщения от пользователя.
    """
    await message.answer(messages.HELP)
