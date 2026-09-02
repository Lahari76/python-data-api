from fastapi import FastAPI

from app.api.routes import router
from app.db.database import Base, engine
from app.models.record import SalesRecord


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Python Data Processing API",
    description=(
        "REST API for ingesting, validating, storing, "
        "retrieving, and analyzing structured sales data."
    ),
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Python Data Processing API",
        "documentation": "/docs"
    }
