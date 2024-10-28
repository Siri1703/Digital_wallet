# app/models.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Wallet(BaseModel):
    user_id: str
    name: str
    email: str
    contact: str
    balance: float = Field(default=0.0)
    status: str = Field(default="active")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    wallet_id: str


class Transaction(BaseModel):
    wallet_id: str
    type: str  # "deposit", "withdrawal", "transfer"
    amount: float
    description: Optional[str] = None
    date: datetime = Field(default_factory=datetime.utcnow)
    source_wallet: Optional[str] = None
    destination_wallet: Optional[str] = None


class User(BaseModel):
    id: Optional[str] = None
    username: str
    password: str  # Ensure to hash passwords
    role: str


class AuditLog(BaseModel):
    action: str
    performed_by: str
    wallet_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class LoginRequest(BaseModel):
    username: str
    password: str
