"""Pydantic схемы."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class DucklingValue(BaseModel):
    """Значение value в ответе."""

    grain: str
    type: str
    value: str
    values: list[DucklingValue] | None = None


class DucklingPayload(BaseModel):
    """Тело запроса Duckling."""

    text: str
    locale: Literal["ru_RU", "en_EN"]
    reftime: int
    dims: list[str] = ["time"]


class DucklingResponse(BaseModel):
    """Данные тела ответа Duckling."""

    body: str
    start: int
    end: int
    value: DucklingValue
    dim: str
    latent: bool
