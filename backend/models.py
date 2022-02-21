import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class EntryModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    duration: int = Field(...)
    night: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "duration": 8,
                "night": "2022-02-06",
            }
        }


class UpdateEntryModel(BaseModel):
    duration: Optional[int]
    night: Optional[str]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {"example": {"duration": 8, "night": "2022-02-06"}}
