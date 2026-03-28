from datetime import date, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_apscheduler.jobstores import DjangoJobStore

from core.settings import EMAIL_HOST_USER
from .models import Reminder


def check_and_send_reminders():
    """Check pending reminders and send email notifications"""
    today = date.today()
    # Filter for pending reminders not yet notified today
    pending = Reminder.objects.filter(is_completed=False)

    for r in pending:
        # Calculate when to send reminder based on due date
        trigger_date = r.due_date - timedelta(days=r.reminder_days_before)

        if trigger_date <= today <= r.due_date:
            # Setup context for email template
            context = {
                'username': r.user.username,
                'title': r.title,
                'amount': r.amount,
                'due_date': r.due_date.strftime('%B %d, %Y'),  # Format date nicely
            }

            # Render HTML template
            html_content = render_to_string('reminder.html', context)

            # Create plain text version for basic email clients
            text_content = strip_tags(html_content)

            try:
                # Create and send email
                email = EmailMultiAlternatives(
                    subject=f"⚠️ Action Required: {r.title} Due Soon",
                    body=text_content,
                    from_email=EMAIL_HOST_USER,
                    to=[r.user.email],
                )

                # Attach HTML version
                email.attach_alternative(html_content, "text/html")

                # Send the email
                email.send()

                # Update record to prevent duplicate emails
                r.save()

            except Exception as e:
                print(f"Failed to send email to {r.user.email}: {e}")


def start_reminder_scheduler():
    """Start background scheduler to send reminders daily"""
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Schedule job to run every day at 08:00 AM
    scheduler.add_job(
        check_and_send_reminders,
        trigger='cron',
        hour=8,
        minute=00,
        id="reminder_job",
        max_instances=1,
        replace_existing=True,
    )
    scheduler.start()