from fastapi import FastAPI

from app.routers import tasks as tasks_router


app = FastAPI(
    title="Study Plan API",
    description="学習計画とタスクを管理するAPI",
    version="0.1.0"
)


app.include_router(tasks_router.router)



@app.get("/")
def title():
    return {"message": "Welcome to the Study Plan API!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}