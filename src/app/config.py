"""Модуль конфигурации бота."""

from typing import Any

import yaml
from pydantic import SecretStr
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    """Класс для хранения настроек приложения.

    Использует Pydantic для валидации и парсинга настроек из файла конфигурации.
    """

    bot_token: SecretStr
    logging_config_path: str

    geonames_username: SecretStr

    # mongo
    mongo_host: str
    mongo_port: int
    mongo_username: str
    mongo_password: SecretStr
    mongo_database: str

    # duckling
    duckling_host: str
    duckling_port: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_logging_config(config_path: str) -> dict[str, Any]:
    """Инициализирует конфигурацию логгера приложения.

    Args:
        config_path: Путь к файлу конфигурации.

    Returns:
        Словарь с конфигурацией логгера.
    """
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)

    return config


bot_config = Settings()  # type: ignore
logging_config = get_logging_config(bot_config.logging_config_path)
