from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base
from routers import users


Base.metadata.create_all(bind=engine)


app = FastAPI(title="Integration with SQL")

app.include_router(users.router)


@app.get("/")
def root(db: Session = Depends(get_db)):
    version = db.execute(text("SELECT version()")).scalar()

    return {
        "message": "Connected!",
        "postgres": version
    }

