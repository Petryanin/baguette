"""Middleware для работы с БД напоминаний."""

from typing import Any
from typing import Awaitable
from typing import Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject

from app.mongo import get_reminder_dal


class ReminderDALMiddleware(BaseMiddleware):
    """Middleware для инъекции зависимости ReminderDAL."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ):
        """Внедряет зависимость ReminderDAL в контекстные данные обработчика."""
        data["reminder_dal"] = get_reminder_dal()
        return await handler(event, data)
