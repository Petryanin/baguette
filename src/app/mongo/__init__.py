__all__ = ("get_reminder_dal",)

from app.mongo.dal import ReminderDAL
from app.config import bot_config


def get_reminder_dal() -> ReminderDAL:
    """Возвращает объект взаимодействия с коллекцией напоминаний."""
    return ReminderDAL(
        bot_config.mongo_host,
        bot_config.mongo_port,
        bot_config.mongo_username,
        bot_config.mongo_password.get_secret_value(),
        bot_config.mongo_database,
    )
