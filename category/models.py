from django.contrib.auth.models import User
from django.db import models

from accounts.constant import AuthFields


class Category(models.Model):

    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column=AuthFields.USER_ID
    )

    name = models.CharField(max_length=100)

    type = models.CharField(max_length=20)

    created_at = models.DateTimeField()

    class Meta:

        managed = False
        db_table = "categories"