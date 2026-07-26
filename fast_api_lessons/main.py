from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Any

from db.database import get_db
from logging_config import get_logger
from routers import users, auth


logger = get_logger(__name__)

app = FastAPI(title="Integration with SQL")

app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root(db: Session = Depends(get_db)) -> dict[str, Any]:
    version = db.execute(text("SELECT version()")).scalar()

    logger.info("Database connected")

    return {
        "message": "Connected!",
        "postgres": version
    }
