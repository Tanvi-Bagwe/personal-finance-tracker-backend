from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.core.mail import send_mail
from datetime import date, timedelta
from .models import Reminder


def check_and_send_reminders():
    today = date.today()
    # Filter: Not completed AND not already notified today
    pending = Reminder.objects.filter(is_completed=False).exclude(last_notified_at=today)

    for r in pending:
        trigger_date = r.due_date - timedelta(days=r.reminder_days_before)

        if trigger_date <= today <= r.due_date:
            try:
                send_mail(
                    subject=f"Action Required: {r.title}",
                    message=f"Hello {r.user.username},\n\nYour payment for '{r.title}' (€{r.amount}) is due on {r.due_date}.",
                    from_email=None,  # Uses DEFAULT_FROM_EMAIL in settings
                    recipient_list=[r.user.email],
                )
                r.last_notified_at = today  # Mark as notified for today
                r.save()
            except Exception as e:
                print(f"Email failed for {r.user.email}: {e}")


def start_reminder_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Run the check every day at 08:00 AM
    scheduler.add_job(
        check_and_send_reminders,
        trigger='cron',
        hour=8,
        minute=0,
        id="reminder_job",
        max_instances=1,
        replace_existing=True,
    )
    scheduler.start()