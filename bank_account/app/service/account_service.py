from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models import Account
from app.schema import AccountCreate, AccountDetail, Transaction


def get_account_by_name(account_name: str, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.account_name == account_name).first()
    return account


def perform_transaction(account: Account, transaction: Transaction):
    if account.version != transaction.version:
        raise HTTPException(
            status_code=409, detail="Conflict, please refresh and try again"
        )

    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid transaction amount")

    return account


def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    try:
        account = Account(account_name=account.account_name, balance=account.balance)
        db.add(account)
        db.commit()
        db.refresh(account)
        return account
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail="Account already exists") from exc


def deposit(account_deposit: Transaction, db: Session = Depends(get_db)):
    account = get_account_by_name(account_deposit.account_name, db)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    account = perform_transaction(account, account_deposit)
    account.balance += account_deposit.amount
    account.version += 1
    db.commit()
    db.refresh(account)
    return account


def withdraw(account_withdraw: Transaction, db: Session = Depends(get_db)):
    account = get_account_by_name(account_withdraw.account_name, db)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    account = perform_transaction(account, account_withdraw)
    if account.balance < account_withdraw.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    account.balance -= account_withdraw.amount
    account.version += 1
    db.commit()
    db.refresh(account)
    return account


def get_account_detail(account: AccountDetail, db: Session = Depends(get_db)):
    account = get_account_by_name(db, account.account_name)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
