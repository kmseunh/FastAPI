from pydantic import BaseModel


class AccountBase(BaseModel):
    account_name: str


class AccountCreate(AccountBase):
    balance: float


class AccountDetail(AccountBase):
    id: int
    balance: float
    version: int

    class Config:
        orm_mode = True


class Transaction(BaseModel):
    account_name: str
    amount: float
    version: int

    class Config:
        orm_mode = True
