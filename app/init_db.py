from app import models
from app.database import engine, Base


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")



if __name__ == "__main__":
    init_db()