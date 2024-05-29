"""Модуль инициализации объектов конфигурации бота."""

import logging.config

from aiogram import Bot
from aiogram import Dispatcher

from app import config
from app.config import bot_config
from app.handlers import router as main_router


logging.info("Initializing all...")
bot = Bot(token=bot_config.bot_token.get_secret_value(), parse_mode="HTML")
dp = Dispatcher()


def init_all() -> None:
    """Инит всех частей сервиса."""
    logging.config.dictConfig(config.logging_config)
    logging.info("Initializing the bot...")

    try:
        register_all_handlers()
    except Exception:
        logging.error("There was an error initializing the bot!")
        raise

    logging.info("Initialization success!")


def register_all_handlers() -> None:
    """Регистрирует все хэндлеры бота."""
    dp.include_router(main_router)
