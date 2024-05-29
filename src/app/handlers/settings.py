"""Обработчики настроек."""

from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.keyboards import reply
from app.misc.states import UserSettings
from app.services import timezone
from app.text import messages


router = Router()


@router.message(Command("settings"))
async def handle_settings_command(message: types.Message) -> None:
    """Обработчик команды `/settings`.

    Args:
        message: Объект сообщения от пользователя.
    """
    await message.answer(
        messages.START,
        reply_markup=reply.get_start_kb(),
    )


@router.message(UserSettings.timezone)
async def handle_user_timezone(
    message: types.Message,
    state: FSMContext,
) -> None:
    """Обработчик обновления часового пояса.

    Args:
        message: Объект сообщения от пользователя.
        state: Состояние контекста FSMContext.
    """
    result = timezone.get(message)

    if result:
        # TODO тут нужно записать в базу
        await state.clear()
        await message.answer(
            f": {result}",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    else:
        await message.answer(
            messages.UNKNOWN_LOCATION, reply_markup=reply.get_start_kb()
        )
