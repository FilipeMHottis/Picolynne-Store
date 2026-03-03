from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from db.models import Cashier
from schemas.cashier import CashierCreate, CashierUpdate, CashierResponse
from services.cashier_service import (
    get_all_cashiers_service,
    get_cashier_by_id_service,
    get_cashier_by_email_service,
    get_cashier_by_name_service,
    create_cashier_service,
    update_cashier_service,
    delete_cashier_service,
)
from core.dependencies import require_admin
from core.security import get_current_user


router = APIRouter(prefix="/cashiers", tags=["Cashiers"])


@router.get("/", response_model=List[CashierResponse])
def get_all_cashiers(db: Session = Depends(get_db)):
    return get_all_cashiers_service(db)


@router.get("/{cashier_id}", response_model=CashierResponse)
def get_cashier_by_id(cashier_id: int, db: Session = Depends(get_db)):
    return get_cashier_by_id_service(db, cashier_id)


@router.get("/email/{email}", response_model=CashierResponse)
def get_cashier_by_email(email: str, db: Session = Depends(get_db)):
    return get_cashier_by_email_service(db, email)


@router.get("/name/{name}", response_model=List[CashierResponse])
def get_cashier_by_name(name: str, db: Session = Depends(get_db)):
    return get_cashier_by_name_service(db, name)


@router.post("/", response_model=CashierResponse)
def create_cashier(
    data: CashierCreate,
    db: Session = Depends(get_db),
    current_user: Cashier = Depends(require_admin),
):
    return create_cashier_service(db, data)


@router.put("/{cashier_id}", response_model=CashierResponse)
def update_cashier(
    cashier_id: int,
    data: CashierUpdate,
    db: Session = Depends(get_db),
    current_user: Cashier = Depends(get_current_user),
):
    return update_cashier_service(db, cashier_id, data, current_user)


@router.delete("/{cashier_id}")
def delete_cashier(
    cashier_id: int,
    db: Session = Depends(get_db),
    current_user: Cashier = Depends(require_admin),
):
    return delete_cashier_service(db, cashier_id, current_user)
