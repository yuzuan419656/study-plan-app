from fastapi import (
    FastAPI, 
    status, 
    Path, 
    HTTPException, 
    Response,
    Depends,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskResponse

app = FastAPI(
    title="Study Plan API",
    description="学習計画とタスクを管理するAPI",
    version="0.1.0"
)




def get_db_task_or_404(
        db: Session,
        task_id: int,
) -> Task:
    db_task = db.get(Task, task_id)

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return db_task



@app.get("/")
def title():
    return {"message": "Welcome to the Study Plan API!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db)
):
    statement = select(Task).order_by(Task.id)
    db_tasks = db.scalars(statement).all()


    return db_tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    return get_db_task_or_404(db, task_id)


@app.post(
        "/tasks", 
        response_model=TaskResponse, 
        status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    ):
    task_data = task.model_dump()
    task_data["status"] = task.status.value

    db_task = Task(**task_data)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


@app.put(
        "/tasks/{task_id}", 
        response_model=TaskResponse,
    )
def update_task(
    updated_task: TaskCreate,
    task_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    db_task = get_db_task_or_404(db, task_id)

    db_task.title = updated_task.title
    db_task.description = updated_task.description
    db_task.status = updated_task.status.value
    db_task.due_date = updated_task.due_date
    db_task.estimated_minutes = updated_task.estimated_minutes

    db.commit()
    db.refresh(db_task)

    return db_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    db_task = get_db_task_or_404(db, task_id)

    db.delete(db_task)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
