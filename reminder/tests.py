from django.test import SimpleTestCase
from unittest.mock import MagicMock
from decimal import Decimal
from datetime import date, timedelta

from reminder.serializers import ReminderSerializer, CreateReminderSerializer


class ReminderSerializerValidation(SimpleTestCase):

    def test_reminder_serializer_returns_all_fields(self):
        mock_reminder = MagicMock()
        mock_reminder.id = 1
        mock_reminder.title = "Pay rent"
        mock_reminder.amount = Decimal('1000.00')
        mock_reminder.due_date = date.today() + timedelta(days=5)
        mock_reminder.reminder_days_before = 2

        serializer = ReminderSerializer(mock_reminder)

        self.assertEqual(serializer.data["id"], 1)
        self.assertEqual(serializer.data["title"], "Pay rent")
        self.assertEqual(serializer.data["amount"], "1000.00")


class CreateReminderSerializerValidation(SimpleTestCase):

    def test_create_reminder_with_valid_data(self):
        future_date = date.today() + timedelta(days=10)
        data = {
            "title": "Pay rent",
            "amount": Decimal('1000.00'),
            "due_date": future_date,
            "reminder_days_before": 2
        }
        serializer = CreateReminderSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["title"], "Pay rent")

    def test_create_reminder_fails_with_past_due_date(self):
        past_date = date.today() - timedelta(days=1)
        data = {
            "title": "Pay rent",
            "amount": Decimal('1000.00'),
            "due_date": past_date,
            "reminder_days_before": 2
        }
        serializer = CreateReminderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("due_date", serializer.errors)

    def test_create_reminder_fails_with_invalid_amount(self):
        future_date = date.today() + timedelta(days=10)
        data = {
            "title": "Pay rent",
            "amount": Decimal('0.00'),
            "due_date": future_date,
            "reminder_days_before": 2
        }
        serializer = CreateReminderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("amount", serializer.errors)

    def test_create_reminder_fails_with_missing_title(self):
        future_date = date.today() + timedelta(days=10)
        data = {
            "amount": Decimal('1000.00'),
            "due_date": future_date,
            "reminder_days_before": 2
        }
        serializer = CreateReminderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_create_reminder_with_default_reminder_days_before(self):
        future_date = date.today() + timedelta(days=10)
        data = {
            "title": "Pay rent",
            "amount": Decimal('1000.00'),
            "due_date": future_date
        }
        serializer = CreateReminderSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["reminder_days_before"], 1)
