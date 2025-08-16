from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CreditResponse(BaseModel):
    user_id: int
    credits: int
    last_updated: datetime


class CreditDelta(BaseModel):
    amount: int = Field(..., ge=1, description="Positive integer amount")


class SchemaUpdate(BaseModel):
    sql: str = Field(..., description="DDL to apply (restricted to ALTER TABLE users/credits ...)")
    

class ErrorResponse(BaseModel):
    detail: str
