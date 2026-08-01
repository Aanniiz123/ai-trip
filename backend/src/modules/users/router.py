
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.modules.users.users_profile import User
from src.modules.auth.service import get_current_active_user, get_password_hash
from src.modules.users.schemas import ProfileRead, ProfileUpdate
from src.modules.users.service import get_or_create_profile, update_profile, update_user, delete_user
from src.modules.users.schemas import UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_me(
    user_data: UserUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    data = user_data.model_dump(exclude_unset=True)
    if "password" in data and data["password"]:
        data["password"] = get_password_hash(data["password"])
    user = update_user(db, current_user.id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    delete_user(db, current_user.id)


@router.get("/me/profile", response_model=ProfileRead)
async def get_profile(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return get_or_create_profile(db, current_user.id)


@router.put("/me/profile", response_model=ProfileRead)
async def upsert_profile(
    profile_data: ProfileUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return update_profile(db, current_user.id, profile_data)
