from datetime import date, time
from uuid import UUID

from pydantic import BaseModel, Field
from src.serialization.schemas.dog import DogSchema
from src.serialization.types import WalkTime
from src.utils.walker_enum import WalkerEnum


class OrderRead(BaseModel):
    """Schema for reading an order from the database."""

    id: UUID = Field(examples=["24d279be-76dc-40d1-a827-411466371fd4"])
    flat: str = Field(examples=["11"])
    dog: DogSchema
    walker: WalkerEnum = Field(examples=[WalkerEnum.PETR.value])
    walk_date: date = Field(examples=["2024-12-22"])
    walk_time: time = Field(examples=["10:00"])


class OrderWrite(BaseModel):
    """Schema for writing an order to the database."""

    flat: str = Field(examples=["11"])
    dog: DogSchema
    walk_date: date = Field(examples=["2024-12-22"])
    walk_time: WalkTime = Field(examples=["10:00"])
