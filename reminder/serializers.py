from decimal import Decimal

from rest_framework import serializers
from .models import Reminder
from .constant import ReminderFields


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'


class CreateReminderSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0.01'))
    due_date = serializers.DateField()
    reminder_days_before = serializers.IntegerField(min_value=0, max_value=30, default=1)

    def validate_due_date(self, value):
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
