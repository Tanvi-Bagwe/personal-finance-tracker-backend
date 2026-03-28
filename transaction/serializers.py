from rest_framework import serializers

from category.constant import CategoryFields
from .constant import TransactionFields
from .models import Transaction


class CreateTransactionSerializer(serializers.Serializer):
    """Serializer for creating and updating transactions"""
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)
    category_id = serializers.IntegerField()
    type = serializers.ChoiceField(choices=[CategoryFields.INCOME, CategoryFields.EXPENSE])
    description = serializers.CharField(max_length=255, required=False, allow_blank=True)
    date = serializers.DateField()


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for displaying transaction data"""
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            TransactionFields.ID,
            TransactionFields.AMOUNT,
            TransactionFields.TYPE,
            TransactionFields.CATEGORY,
            TransactionFields.CATEGORY_NAME,
            TransactionFields.DESCRIPTION,
            TransactionFields.DATE
        ]
