from fastapi import FastAPI, status, Path, HTTPException

from app.schemas import TaskCreate, TaskResponse

app = FastAPI(
    title="Study Plan API",
    description="学習計画とタスクを管理するAPI",
    version="0.1.0"
)


tasks: list[TaskResponse] = []


@app.get("/")
def title():
    return {"message": "Welcome to the Study Plan API!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int = Path(gt=0)
):
    task = next(
        (task for task in tasks if task.id == task_id),
        None,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@app.post(
        "/tasks", 
        response_model=TaskResponse, 
        status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    new_task = TaskResponse(
        id=len(tasks) + 1,
        **task.model_dump(),
    )

    tasks.append(new_task)
    return new_task