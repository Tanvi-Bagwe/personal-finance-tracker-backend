from django.db import models
from django.contrib.auth.models import User
from accounts.constant import AuthFields

class Reminder(models.Model):
    """Store bill and payment reminders for users"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column=AuthFields.USER_ID)
    title = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    due_date = models.DateField()
    reminder_days_before = models.IntegerField(default=1)
    is_read = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "reminders"