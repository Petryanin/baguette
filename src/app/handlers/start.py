"""Обработка сообщений от пользователя при старте бота."""

from aiogram import Router
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from app.keyboards import reply
from app.misc.states import Start
from app.services import timezone
from app.text import messages


router = Router()


@router.message(CommandStart())
async def handle_start_command(message: types.Message, state: FSMContext) -> None:
    """Обработчик команды `/start`.

    Args:
        message: Объект сообщения от пользователя.
        state: Состояние контекста FSMContext.
    """
    # TODO добавить условие
    await state.set_state(Start.timezone)
    await message.answer(
        f"{messages.START}{messages.TIMEZONE_REQUEST}",
        reply_markup=reply.get_start_kb(),
    )


@router.message(Start.timezone)
async def handle_start_timezone(message: types.Message, state: FSMContext) -> None:
    """Обработчик первичной настройки часового пояса.

    Args:
        message: Объект сообщения от пользователя.
        state: Состояние контекста FSMContext.
    """
    timezone_data = await timezone.get(message)

    if timezone_data:
        # TODO тут нужно записать в базу
        await state.clear()
        tz, time = timezone.get_pretty_tz_and_time(timezone_data.raw)

        await message.answer(
            messages.CURRENT_SETTINGS.format(tz, time),
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=reply.get_main_kb(),
        )
    else:
        await message.answer(
            messages.UNKNOWN_LOCATION, reply_markup=reply.get_start_kb()
        )
