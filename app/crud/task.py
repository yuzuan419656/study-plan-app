from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task



def get_tasks(db: Session) -> list[Task]:
    statement = select(Task).order_by(Task.id)
    return list(db.scalars(statement).all())


def get_task_by_id(
        db: Session,
        task_id: int,
) -> Task | None:
    return db.get(Task, task_id)