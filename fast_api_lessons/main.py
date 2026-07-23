from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db
from routers import users


# Base.metadata.create_all(bind=engine)


app = FastAPI(title="Integration with SQL")

app.include_router(users.router)


@app.get("/")
def root(db: Session = Depends(get_db)) -> dict[str, str]:
    version = db.execute(text("SELECT version()")).scalar()

    return {
        "message": "Connected!",
        "postgres": version
    }

