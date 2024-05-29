"""Обработчики сообщений от пользователя."""

from aiogram import F
from aiogram import Router
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from app.middlewares.reminder_dal import ReminderDALMiddleware
from app.misc import states
from app.mongo.dal import ReminderDAL
from app.services import duckling
from app.text import buttons
from app.text import messages


router = Router()
router.message.middleware(ReminderDALMiddleware())


@router.message(F.text == buttons.ADD)
async def handle_add(message: types.Message, state: FSMContext) -> None:
    """Обработчик кнопки Добавить.

    Args:
        message: Объект сообщения от пользователя.
        state: Состояние контекста FSMContext.
    """
    await state.set_state(states.Add.text)
    await message.answer(messages.ENTER_REMINDER, reply_markup=ReplyKeyboardRemove())


@router.message(states.Add.text)
async def handle_reminder(
    message: types.Message,
    state: FSMContext,
    reminder_dal: ReminderDAL,
) -> None:
    """Обработчик сообщения с напоминанием.

    Args:
        message: Объект сообщения от пользователя.
        state: Состояние контекста FSMContext.
        reminder_dal: Объект взаимодействия с БД.
    """
    if not message.text:
        await message.answer(messages.INVALID_REMINDER)
        return

    await state.clear()

    text, date_time = await duckling.parse(message.text)
    await reminder_dal.create_reminder({"text": text, "date_time": date_time})
    await message.answer(messages.REMINDER_ADDED)
