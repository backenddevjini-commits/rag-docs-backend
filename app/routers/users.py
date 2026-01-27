from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # 1. 이메일 중복 체크
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. 비밀번호 해싱
    hashed_pw = hash_password(user.password)

    # 3. 유저 생성
    new_user = User(
        email=user.email,
        hashed_password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "created_at": new_user.created_at
    }