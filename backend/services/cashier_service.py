from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.models import Cashier
from schemas.cashier import CashierCreate, CashierUpdate
from core.security import hash_password


def get_all_cashiers_service(db: Session) -> List[Cashier]:
    return db.query(Cashier).filter(Cashier.status == True).all()


def get_cashier_by_id_service(db: Session, cashier_id: int) -> Cashier:
    cashier = (
        db.query(Cashier)
        .filter(Cashier.id == cashier_id, Cashier.status == True)
        .first()
    )

    if not cashier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )

    return cashier


def get_cashier_by_email_service(db: Session, email: str) -> Cashier:
    cashier = (
        db.query(Cashier)
        .filter(Cashier.email == email, Cashier.status == True)
        .first()
    )

    if not cashier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )

    return cashier


def get_cashier_by_name_service(db: Session, name: str) -> List[Cashier]:
    cashiers = (
        db.query(Cashier)
        .filter(Cashier.name.ilike(f"%{name}%"), Cashier.status == True)
        .all()
    )

    if not cashiers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum usuário encontrado com esse nome",
        )

    return cashiers


def create_cashier_service(db: Session, data: CashierCreate):
    # Verifica se já existe email
    existing = db.query(Cashier).filter(Cashier.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado",
        )

    new_cashier = Cashier(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        role=data.role,
    )

    db.add(new_cashier)
    db.commit()
    db.refresh(new_cashier)

    return new_cashier


def update_cashier_service(
    db: Session,
    cashier_id: int,
    data: CashierUpdate,
    current_user: Cashier,
):
    cashier = db.query(Cashier).filter(Cashier.id == cashier_id).first()

    if not cashier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )
    
    # Verifica se o email já existe para outro usuário
    if data.email is not None and data.email != cashier.email:
        existing = db.query(Cashier).filter(Cashier.email == data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado para outro usuário",
            )

    # 🔐 Regra de autorização
    if current_user.role != "admin":
        # Só pode editar a si mesmo
        if current_user.id != cashier.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para alterar este usuário",
            )

        # Não pode alterar role
        if data.role is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não pode alterar sua própria role",
            )

    # 🔄 Atualizações permitidas
    if data.name is not None:
        cashier.name = data.name

    if data.email is not None:
        cashier.email = data.email

    if data.password is not None:
        cashier.password = hash_password(data.password)

    if data.role is not None and current_user.role == "admin":
        cashier.role = data.role

    db.commit()
    db.refresh(cashier)

    return cashier


def delete_cashier_service(db: Session, cashier_id: int, current_user: Cashier):
    cashier = db.query(Cashier).filter(Cashier.id == cashier_id).first()

    if not cashier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )
        
    if cashier.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Você não pode deletar seu próprio usuário"
        )
        
    if cashier.role == "admin":
        raise HTTPException(
            status_code=403,
            detail="Não é permitido deletar outro administrador"
        )

    cashier.status = False
    db.commit()
    db.refresh(cashier)

    return {"message": "Usuário desativado com sucesso"}