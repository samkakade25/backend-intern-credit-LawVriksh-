from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from .db import SessionLocal
from .crud import add_daily_to_all

scheduler: BackgroundScheduler | None = None

def _job():
    with SessionLocal() as db:  # type: Session
        add_daily_to_all(db, delta=5)

def start_scheduler():
    global scheduler
    if scheduler is None:
        scheduler = BackgroundScheduler(timezone="UTC")
        # Run daily at 00:00 UTC
        scheduler.add_job(_job, trigger=CronTrigger(hour=0, minute=0))
        scheduler.start()

def shutdown_scheduler():
    global scheduler
    if scheduler:
        scheduler.shutdown(wait=False)
        scheduler = None
