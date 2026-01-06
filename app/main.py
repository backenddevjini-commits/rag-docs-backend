from fastapi import FastAPI
from app.routers import health, documents

app = FastAPI()

app.include_router(health.router)
app.include_router(documents.router)