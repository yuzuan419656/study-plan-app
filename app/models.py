from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Task(Base):
    __tablename__="tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="not_started"
    )

    due_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    estimated_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

