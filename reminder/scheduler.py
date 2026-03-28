from datetime import date, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_apscheduler.jobstores import DjangoJobStore

from core.settings import EMAIL_HOST_USER
from .models import Reminder


def check_and_send_reminders():
    today = date.today()
    # Filter for pending reminders not yet notified today
    pending = Reminder.objects.filter(is_completed=False)

    for r in pending:
        trigger_date = r.due_date - timedelta(days=r.reminder_days_before)

        if trigger_date <= today <= r.due_date:
            # 1. Setup Context Data for the HTML template
            context = {
                'username': r.user.username,
                'title': r.title,
                'amount': r.amount,
                'due_date': r.due_date.strftime('%B %d, %Y'),  # Prettier date format
            }

            # 2. Render HTML to a string
            html_content = render_to_string('reminder.html', context)

            # 3. Create Plain Text version (fallback for basic email clients)
            text_content = strip_tags(html_content)

            try:
                # 4. Create the Email Object
                email = EmailMultiAlternatives(
                    subject=f"⚠️ Action Required: {r.title} Due Soon",
                    body=text_content,  # The backup text
                    from_email=EMAIL_HOST_USER,
                    to=[r.user.email],
                )

                # 5. Attach the HTML version
                email.attach_alternative(html_content, "text/html")

                # 6. Send
                email.send()

                # Stamp the record to prevent duplicate emails today
                r.last_notified_at = today
                r.save()

            except Exception as e:
                print(f"Failed to send email to {r.user.email}: {e}")


def start_reminder_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Run the check every day at 08:00 AM
    scheduler.add_job(
        check_and_send_reminders,
        trigger='cron',
        hour=7,
        minute=42,
        id="reminder_job",
        max_instances=1,
        replace_existing=True,
    )
    scheduler.start()