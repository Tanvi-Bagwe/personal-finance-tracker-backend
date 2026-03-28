import os
from django.apps import AppConfig


class ReminderConfig(AppConfig):
    """Configuration for the reminder app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reminder'

    def ready(self):
        """Initialize scheduler when app is ready"""
        # Skip scheduler during migrations
        if os.environ.get('RUN_MAIN') != 'true':
            return

        from django.core.management import execute_from_command_line
        import sys

        # Don't start scheduler during migrations
        if 'migrate' not in sys.argv:
            from .scheduler import start_reminder_scheduler
            start_reminder_scheduler()