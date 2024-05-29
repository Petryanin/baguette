"""Функционал взаимодействия с хранилищем напоминаний."""

import logging
from typing import Any
from typing import Mapping

import motor.motor_asyncio
from pymongo.errors import PyMongoError

from app.misc.singleton import SingletonMeta


class ReminderDAL(metaclass=SingletonMeta):
    """Класс для взаимодействия с коллекцией напоминаний в MongoDB."""

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        database: str,
    ) -> None:
        """Инициализация клиента MongoDB и выбор базы данных.

        Args:
            host: Хост MongoDB.
            port: Порт MongoDB.
            username: Имя пользователя для подключения к MongoDB.
            password: Пароль для подключения к MongoDB.
            database: Имя базы данных MongoDB.
        """
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            host=host,
            port=port,
            username=username,
            password=password,
        )
        self.db = self.client[database]
        self.reminders_collection = self.db["reminders"]

    async def create_reminder(self, reminder_data: dict) -> str | None:
        """Создает новое напоминание в коллекции.

        Args:
            reminder_data: Данные напоминания для вставки.

        Returns:
            ID созданного напоминания или None, если произошла ошибка.
        """
        try:
            result = await self.reminders_collection.insert_one(reminder_data)
            return result.inserted_id
        except PyMongoError:
            logging.exception("Error creating reminder")
            return None

    async def get_reminder(self, reminder_id: str) -> dict | None:
        """Возвращает напоминание по его идентификатору.

        Args:
            reminder_id: Идентификатор напоминания.

        Returns:
            Документ напоминания, если найден, иначе None.
        """
        try:
            return await self.reminders_collection.find_one({"_id": reminder_id})
        except PyMongoError:
            logging.exception("Error fetching reminder")
            return None

    async def update_reminder(
        self, reminder_id: str, update_data: dict
    ) -> Mapping[str, Any] | None:
        """Обновляет существующее напоминание.

        Args:
            reminder_id: Идентификатор напоминания.
            update_data: Данные для обновления.

        Returns:
            Обновленный документ напоминания, если обновление прошло успешно,
            иначе None.
        """
        try:
            result = await self.reminders_collection.update_one(
                {"_id": reminder_id}, {"$set": update_data}
            )
            return result.raw_result
        except PyMongoError:
            logging.exception("Error updating reminder")
            return None

    async def delete_reminder(self, reminder_id: str) -> bool:
        """Удаляет напоминание по его идентификатору.

        Args:
            reminder_id: Идентификатор напоминания.

        Returns:
            True, если удаление прошло успешно, иначе False.
        """
        try:
            result = await self.reminders_collection.delete_one({"_id": reminder_id})
            return result.deleted_count > 0
        except PyMongoError:
            logging.exception("Error deleting reminder")
            return False
