from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schema import AccountCreate, AccountDetail, Transaction
from app.service.account_service import (
    create_account,
    deposit,
    get_account_detail,
    withdraw,
)

router = APIRouter(prefix="/accounts")


@router.post("/create/")
async def create_account_route(account: AccountCreate, db: Session = Depends(get_db)):
    return create_account(account, db)


@router.post("/{account_number}/deposit/")
async def deposit_route(account: Transaction, db: Session = Depends(get_db)):
    return deposit(account, db)


@router.post("/{account_number}/withdraw/")
async def withdraw_route(account: Transaction, db: Session = Depends(get_db)):
    return withdraw(account, db)


@router.get("/accounts/{account_number}/")
async def get_account_route(account: AccountDetail, db: Session = Depends(get_db)):
    return get_account_detail(account, db)
