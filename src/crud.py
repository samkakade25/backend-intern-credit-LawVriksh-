from datetime import datetime, timezone
from sqlalchemy import select, update, insert
from sqlalchemy.orm import Session
from .models import Credit, User


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc).replace(tzinfo=None)  # store naive UTC in DB


def ensure_credit_row(db: Session, user_id: int) -> None:
    # Create a credits row if missing (idempotent)
    exists = db.execute(select(Credit).where(Credit.user_id == user_id)).scalar_one_or_none()
    if exists is None:
        # Check user exists
        user = db.execute(select(User.user_id).where(User.user_id == user_id)).scalar_one_or_none()
        if user is None:
            raise ValueError("User not found")
        db.execute(insert(Credit).values(user_id=user_id, credits=0, last_updated=_utcnow()))


def get_credit(db: Session, user_id: int) -> Credit:
    ensure_credit_row(db, user_id)
    credit = db.execute(select(Credit).where(Credit.user_id == user_id)).scalar_one()
    return credit


def add_credits(db: Session, user_id: int, amount: int) -> Credit:
    ensure_credit_row(db, user_id)
    db.execute(
        update(Credit)
        .where(Credit.user_id == user_id)
        .values(credits=Credit.credits + amount, last_updated=_utcnow())
    )
    db.commit()
    return get_credit(db, user_id)


def deduct_credits(db: Session, user_id: int, amount: int) -> Credit:
    ensure_credit_row(db, user_id)
    current = db.execute(select(Credit).where(Credit.user_id == user_id)).scalar_one()
    if current.credits - amount < 0:
        raise ValueError("Insufficient balance")
    db.execute(
        update(Credit)
        .where(Credit.user_id == user_id)
        .values(credits=current.credits - amount, last_updated=_utcnow())
    )
    db.commit()
    return get_credit(db, user_id)


def reset_credits(db: Session, user_id: int) -> Credit:
    ensure_credit_row(db, user_id)
    db.execute(
        update(Credit)
        .where(Credit.user_id == user_id)
        .values(credits=0, last_updated=_utcnow())
    )
    db.commit()
    return get_credit(db, user_id)


def add_daily_to_all(db: Session, delta: int = 5) -> int:
    """Add `delta` credits to all users who have a credits row. Return affected rows."""
    result = db.execute(
        update(Credit)
        .values(credits=Credit.credits + delta, last_updated=_utcnow())
    )
    db.commit()
    return result.rowcount or 0
