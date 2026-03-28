from django.contrib.auth.models import User
from django.db import models

from category.models import Category


from django.contrib.auth.models import User
from django.db import models
from accounts.constant import AuthFields
from .models import Category # Assuming Category is in the same app or imported

class Transaction(models.Model):
    """Store financial transactions (income/expense) for each user"""
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column=AuthFields.USER_ID
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        db_column="category_id"
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=20)
    description = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "transactions"