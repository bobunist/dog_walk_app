from pydantic import BaseModel, Field


class DogSchema(BaseModel):
    """Schema for reading a dog from the database."""

    breed: str = Field(examples=["Алабай"])
    name: str = Field(examples=["Бобик"])
