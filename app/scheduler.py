from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.monthly_report import send_monthly_report

def send_email_summary():
    db: Session = SessionLocal()
    try:
        send_monthly_report(db)
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_email_summary, trigger="cron", day="last", hour=23, minute=59)
    scheduler.start()