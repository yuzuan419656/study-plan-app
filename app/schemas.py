from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class TaskStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None  = Field(default=None, max_length=500)
    status: TaskStatus = TaskStatus.NOT_STARTED
    due_date: date | None = None
    estimated_minutes: int = Field(gt=0)


class TaskResponse(TaskCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
    