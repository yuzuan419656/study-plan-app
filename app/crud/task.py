from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreate



def get_tasks(db: Session) -> list[Task]:
    statement = select(Task).order_by(Task.id)
    return list(db.scalars(statement).all())


def get_task_by_id(
        db: Session,
        task_id: int,
) -> Task | None:
    return db.get(Task, task_id)


def create_task(
        db:Session,
        task: TaskCreate,
) -> Task:
    task_data = task.model_dump()
    task_data["status"] = task.status.value

    db_task = Task(**task_data)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task