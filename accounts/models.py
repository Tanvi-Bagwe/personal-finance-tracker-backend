# Models for user authentication and profile management
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from accounts.constant import AuthFields


class UserProfile(models.Model):
    """Store additional user profile information"""
    id = models.AutoField(primary_key=True)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_column=AuthFields.USER_ID
    )

    phone = models.CharField(max_length=20, null=True)

    currency = models.CharField(max_length=10, default="EUR")

    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "user_profiles"


class PasswordResetOTP(models.Model):
    """Store OTP for password reset"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'password_reset_otp'

    def is_expired(self):
        # Check if OTP is older than 10 minutes
        return timezone.now() > self.created_at + datetime.timedelta(minutes=10)
