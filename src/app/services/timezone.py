"""Функционал определения часового пояса пользователя."""

from aiogram import types
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import GeoNames
from geopy.timezone import Timezone

from app.config import bot_config


async def get_from_coords(coords: str) -> Timezone | None:
    """Возвращает часовой пояс по координатам.

    Args:
        coords: Координаты.

    Returns:
        Объект часового пояса.
    """
    async with GeoNames(
        username=bot_config.geonames_username.get_secret_value(),
        adapter_factory=AioHTTPAdapter,
    ) as geolocator:
        timezone = await geolocator.reverse_timezone(coords)

    return timezone


async def get_from_location_name(location_name: str) -> Timezone | None:
    """Возвращает часовой пояс по названию локации.

    Args:
        location_name: Название локации.

    Returns:
        Объект часового пояса.
    """
    async with GeoNames(
        username=bot_config.geonames_username.get_secret_value(),
        adapter_factory=AioHTTPAdapter,
    ) as geolocator:
        location = await geolocator.geocode(location_name)

    return (
        await get_from_coords(f"{location.latitude}, {location.longitude}")
        if location
        else None
    )


async def get(message: types.Message) -> Timezone | None:
    """Возвращает часовой пояс по объекту сообщения Telegram.

    Args:
        message: Сообщение.

    Returns:
        Объект часового пояса.
    """
    result = None

    if message.text:
        result = await get_from_location_name(message.text)
    elif message.location:
        result = await get_from_coords(
            f"{message.location.latitude}, {message.location.longitude}"
        )

    return result


def get_pretty_tz_and_time(timezone_data: dict) -> tuple[str, str]:
    """Возвращает красивое строковое представление ЧП и локального времени.

    Args:
        timezone_data: Словарь с данными о часовом поясе.

    Returns:
        Кортеж из двух строк.
    """
    tz_id = timezone_data["timezoneId"]
    gmt_offset = timezone_data["gmtOffset"]
    time = timezone_data["time"]

    pretty_tz = f"{tz_id} \({"\+" if gmt_offset >= 0 else "\-"}{gmt_offset}\)"
    pretty_time = f"{time.split(" ")[-1]}"

    return pretty_tz, pretty_time
