from fastapi import FastAPI
from app.routers.documents import router as documents_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(documents_router)