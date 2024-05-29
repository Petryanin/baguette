"""Пакет обработчиков сообщений."""

__all__ = ("router",)

from aiogram import Router

from app.handlers.help import router as help_router
from app.handlers.start import router as start_router
from app.handlers.add import router as user_router
from app.handlers.settings import router as settings_router

router = Router()

router.include_routers(
    start_router,
    help_router,
    settings_router,
    user_router,
)


# @router.message()
# async def process_unknown_msg(message: types.Message) -> None:
#     """Обработчик непонятного сообщения.

#     Args:
#         message: Объект сообщения от пользователя.
#     """
#     await message.answer(messages.UNKNOWN)
