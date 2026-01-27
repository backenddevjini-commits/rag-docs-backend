from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.routers.health import router as health_router
from app.routers.documents import router as documents_router
from app.routers.users import router as users_router
from app.db.database import engine, Base
from app.db import models

from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler
)

app = FastAPI()

# 에러 핸들러 등록
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# (임시) 테이블 생성
Base.metadata.create_all(bind=engine)

# 라우터 등록
app.include_router(health_router)
app.include_router(documents_router)
app.include_router(users_router)