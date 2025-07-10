from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional


class Account(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    balance: float = 0.0


class AccountCreate(BaseModel):
    name: str


class Transaction(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    from_account: UUID
    to_account: UUID
    amount: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    note: Optional[str] = None


class TransactionCreate(BaseModel):
    from_account: UUID
    to_account: UUID
    amount: float
    note: Optional[str] = None
