from fastapi import Depends, HTTPException, status
from core.security import get_current_user
from db.models import Cashier

def require_admin(current_user: Cashier = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem realizar esta ação"
        )
    return current_user