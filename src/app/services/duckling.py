"""Модуль взаимодействия с Duckling."""

import time

import httpx

from app.config import bot_config


URL = f"{bot_config.duckling_host}:{bot_config.duckling_port}"


async def parse(text: str):
    """Возвращает распарсенный текст с напоминанием и датой."""
    duckling_url = f"{URL}/parse"

    # Параметры запроса
    data = {"text": text, "locale": "ru_RU", "reftime": int(time.time() * 1000)}

    async with httpx.AsyncClient() as client:
        response = await client.post(duckling_url, data=data)
        parsed_data = response.json()

    # Извлечение временных выражений
    date_time = None
    if parsed_data:
        for item in parsed_data:
            if item["dim"] == "time":
                date_time = item["value"]["value"]
                text = text.replace(item["body"], "").strip()

    return text, date_time
