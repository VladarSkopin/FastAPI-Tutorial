from fastapi import Depends, HTTPException, status

from constants import UserRole
from dependencies import get_current_active_user
from db.models import User


def require_sysadmin(
    current_user: User = Depends(get_current_active_user),
) -> User:

    if current_user.role != UserRole.SYSADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return current_user


def require_ml_engineer(
    current_user: User = Depends(get_current_active_user),
) -> User:

    if current_user.role != UserRole.MLENGINEER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return current_user


def require_scientist(
    current_user: User = Depends(get_current_active_user),
) -> User:

    if current_user.role != UserRole.SCIENTIST:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return current_user


def require_roles(*allowed_roles: UserRole):

    def checker(
        current_user: User = Depends(get_current_active_user),
    ) -> User:

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        return current_user

    return checker
