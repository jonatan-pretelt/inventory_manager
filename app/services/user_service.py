from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models
from app.exceptions import DuplicateUserError, InvalidCredentialsError
from app.core import security
import logging
from sqlalchemy import select
from typing import cast

logger = logging.getLogger(__name__)


def create_user(db: Session, email: str, password: str):
    user = models.UserDB(email=email, hashed_password=security.hash_password(password))
    db.add(user)

    try:
        db.flush()
    except IntegrityError:
        logger.warning("Duplicate User attempted", extra={"email": user.email})
        raise DuplicateUserError("User already exists")

    return user


def authenticate_user(db: Session, email: str, password: str):
    stmt = select(models.UserDB)
    stmt = stmt.where(models.UserDB.email == email)
    result = db.execute(stmt)
    user = result.scalars().first()
    if not user or not security.verify_password(
        password, cast(str, user.hashed_password)
    ):
        raise InvalidCredentialsError("Invalid credentials")

    return user
