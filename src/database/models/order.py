from datetime import date, time
from uuid import UUID, uuid4

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel
from src.utils.walker_enum import WalkerEnum


class OrderModel(SQLModel, table=True):
    """Model for an order in the database."""

    __tablename__ = "order"
    __table_args__ = (
        UniqueConstraint("walker", "walk_date", "walk_time", name="walker_date_time"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    flat: str
    walker: WalkerEnum
    dog_name: str
    dog_breed: str
    walk_date: date
    walk_time: time
