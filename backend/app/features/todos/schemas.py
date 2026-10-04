from datetime import date, datetime
from enum import Enum
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, model_validator

from .validators import validate_patch_fields, validate_title


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TodoCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: Annotated[str, AfterValidator(validate_title)] = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=2000)
    priority: Priority = Priority.medium
    due_date: date | None = None
    completed: bool = Field(default=False, strict=True)


class TodoUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: Annotated[str | None, AfterValidator(validate_title)] = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    priority: Priority | None = None
    due_date: date | None = None
    completed: bool | None = Field(default=None, strict=True)

    @model_validator(mode="after")
    def validate_patch(self):
        return validate_patch_fields(self)


class Todo(TodoCreate):
    id: int
    created_at: datetime
    updated_at: datetime
