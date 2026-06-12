# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy import select

from database import get_db

from models.user import User

from schemas.user import (
    RegisterRequest,
    TokenResponse,
    UserOut
)

from utils.auth import (
    hash_password,
    verify_password,
    create_access_token
)

from dependencies import get_current_user

# ── Router ────────────────────────────────────────────────────────────────
router = APIRouter()

# ── POST /auth/register ───────────────────────────────────────────────────
@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_user = db.execute(
        select(User).where(
            User.email == data.email
        )
    ).scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    new_user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user

# ── POST /auth/login ──────────────────────────────────────────────────────
@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.execute(
        select(User).where(
            User.email == form.username,
            User.is_active == True
        )
    ).scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(
        form.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token({
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ── GET /auth/me ──────────────────────────────────────────────────────────
@router.get(
    "/me",
    response_model=UserOut
)
def me(
    current_user: User = Depends(get_current_user)
):

    return current_user