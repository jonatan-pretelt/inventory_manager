from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserResponse #, ProductCreate, ProductUpdate
from app.services import user_service
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    with db.begin():
        logger.info("Creating user", extra={"email": user.email})
        user = user_service.create_user( db,user.email, user.password)
        db.refresh(user)
        return user
