from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.crud import task as task_crud
from app.database import get_db
from app.schemas import TaskCreate, TaskResponse


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get(
    "",
    response_model=list[TaskResponse]
)
def get_tasks(
    db:Session = Depends(get_db),
):
    return task_crud.get_tasks(db)



@router.get(
    "/{task_id}",
    response_model=TaskResponse, 
)
def get_task(
    task_id: int = Path(gt=0),
    db:Session = Depends(get_db),
):
    db_task = task_crud.get_task_by_id(db, task_id)

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        ) 

    return db_task


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
):
    return task_crud.create_task(db, task)