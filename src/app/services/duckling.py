"""Модуль взаимодействия с Duckling."""

import time

import httpx

from app.config import bot_config
from app.misc import schemas


URL = f"{bot_config.duckling_host}:{bot_config.duckling_port}"


async def parse(text: str):
    """Возвращает распарсенный текст с напоминанием и датой."""
    payload = schemas.DucklingPayload(
        text=text,
        locale="ru_RU",
        reftime=int(time.time() * 1000),
    )

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{URL}/parse", data=payload.model_dump())
        response_json = response.json()
        response_data = (
            schemas.DucklingResponse(**response_json[0]) if response_json else None
        )

    date_time = None
    if response_data:
        date_time = response_data.value.value
        text = text.replace(response_data.body, "").strip()

    return text, date_time
