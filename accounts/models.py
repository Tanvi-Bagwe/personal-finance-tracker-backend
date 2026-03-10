from django.contrib.auth.models import AbstractUser, User
from django.db import models

class UserProfile(models.Model):

    id = models.AutoField(primary_key=True)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_column="user_id"
    )

    phone = models.CharField(max_length=20, null=True)

    currency = models.CharField(max_length=10, default="EUR")

    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "user_profiles"