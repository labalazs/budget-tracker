from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.services.stats import get_stats
from app.services.email_service import send_email

def send_monthly_report(db: Session):
    today = datetime.utcnow()
    first_day = today.replace(day=1)
    last_day = today
    by_category, monthly = get_stats(db=db, date_from=first_day, date_to=last_day)
    lines = ["Monthly Financial Summary\n"]
    lines.append("By category:\n")
    for item in by_category:
        lines.append(f'- {item["category"]}: {item["total_amount"]}\n')
    lines.append("Summary:\n")
    for item in monthly:
        lines.append(f'- {item["category"]}: {item["total_amount"]}\n')
    body = "\n".join(lines)
    send_email(subject="Monthly Finance Report", body=body)
    