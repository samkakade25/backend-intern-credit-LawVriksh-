from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from .db import Base, engine, get_db
from .models import *  # noqa
from .schemas import CreditResponse, CreditDelta, SchemaUpdate, ErrorResponse
from .crud import get_credit, add_credits, deduct_credits, reset_credits
from .tasks import start_scheduler, shutdown_scheduler
import re
from pydantic import BaseModel


app = FastAPI(title="Credit Management API", version="1.0.0")

# CORS (adjust origins for your frontends)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SchemaUpdateRequest(BaseModel):
    operation: str
    table: str
    column: str
    type: str = None
    default: int = None

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def on_startup():
    start_scheduler()


@app.on_event("shutdown")
def on_shutdown():
    shutdown_scheduler()


# ---------- Credit APIs ----------

@app.get("/api/credits/{user_id}", response_model=CreditResponse, responses={404: {"model": ErrorResponse}})
def api_get_credit(user_id: int, db: Session = Depends(get_db)):
    try:
        c = get_credit(db, user_id)
        return CreditResponse(user_id=c.user_id, credits=c.credits, last_updated=c.last_updated)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/api/credits/{user_id}/add", response_model=CreditResponse, responses={404: {"model": ErrorResponse}})
def api_add_credit(user_id: int, payload: CreditDelta, db: Session = Depends(get_db)):
    try:
        c = add_credits(db, user_id, payload.amount)
        return CreditResponse(user_id=c.user_id, credits=c.credits, last_updated=c.last_updated)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/api/credits/{user_id}/deduct", response_model=CreditResponse,
          responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}})
def api_deduct_credit(user_id: int, payload: CreditDelta, db: Session = Depends(get_db)):
    try:
        c = deduct_credits(db, user_id, payload.amount)
        return CreditResponse(user_id=c.user_id, credits=c.credits, last_updated=c.last_updated)
    except ValueError as e:
        msg = str(e)
        if msg == "User not found":
            raise HTTPException(status_code=404, detail=msg)
        else:
            raise HTTPException(status_code=400, detail=msg)


@app.patch("/api/credits/{user_id}/reset", response_model=CreditResponse, responses={404: {"model": ErrorResponse}})
def api_reset_credit(user_id: int, db: Session = Depends(get_db)):
    try:
        c = reset_credits(db, user_id)
        return CreditResponse(user_id=c.user_id, credits=c.credits, last_updated=c.last_updated)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")


# ---------- Dynamic Schema Update (SAFE-GUARDED) ----------
# Only allow ALTER TABLE on 'users' or 'credits', single statement, no DML.

ALTER_RE = re.compile(
    r"^\s*ALTER\s+TABLE\s+(users|credits)\s+.+;$",
    flags=re.IGNORECASE | re.DOTALL
)

@app.post("/api/schema/update", responses={400: {"model": ErrorResponse}})
def api_schema_update(body: SchemaUpdate, db: Session = Depends(get_db)):
    sql = body.sql.strip()
    # Require trailing semicolon and forbid multiple statements
    if sql.count(";") != 1:
        raise HTTPException(status_code=400, detail="Exactly one statement is allowed.")
    if not ALTER_RE.match(sql):
        raise HTTPException(
            status_code=400,
            detail="Only 'ALTER TABLE users|credits ...;' statements are permitted."
        )
    try:
        db.execute(text(sql))
        db.commit()
        return {"status": "ok", "applied": sql}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"DDL error: {e}")
    

@app.patch("/api/credits/external-update")
def external_update(req: SchemaUpdateRequest):
    # Example: just a placeholder
    # Implement dynamic ALTER TABLE logic here
    if req.operation == "add_column":
        # Execute raw SQL to add column
        return {"message": f"Column '{req.column}' added to '{req.table}' successfully"}
    else:
        raise HTTPException(status_code=400, detail="Unsupported operation")
