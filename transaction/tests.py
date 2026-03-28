from django.test import SimpleTestCase
from unittest.mock import MagicMock
from decimal import Decimal
from datetime import date

from transaction.serializers import TransactionSerializer, CreateTransactionSerializer
from transaction.constant import TransactionFields
from category.constant import CategoryFields


class TransactionSerializerValidation(SimpleTestCase):

    def test_transaction_serializer_returns_all_fields(self):
        mock_category = MagicMock()
        mock_category.name = "Groceries"

        mock_transaction = MagicMock()
        mock_transaction.id = 1
        mock_transaction.amount = Decimal('50.00')
        mock_transaction.type = CategoryFields.EXPENSE
        mock_transaction.category = mock_category
        mock_transaction.description = "Weekly shopping"
        mock_transaction.date = date.today()

        serializer = TransactionSerializer(mock_transaction)

        self.assertEqual(serializer.data["id"], 1)
        self.assertEqual(serializer.data["amount"], "50.00")
        self.assertEqual(serializer.data["type"], CategoryFields.EXPENSE)
        self.assertEqual(serializer.data["category_name"], "Groceries")
        self.assertEqual(serializer.data["description"], "Weekly shopping")


class CreateTransactionSerializerValidation(SimpleTestCase):

    def test_create_transaction_with_valid_data(self):
        data = {
            "amount": Decimal('100.00'),
            "category_id": 1,
            "type": CategoryFields.EXPENSE,
            "description": "Groceries",
            "date": date.today()
        }
        serializer = CreateTransactionSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["amount"], Decimal('100.00'))

    def test_create_transaction_fails_with_invalid_amount(self):
        data = {
            "amount": Decimal('0.00'),
            "category_id": 1,
            "type": CategoryFields.EXPENSE,
            "description": "Groceries",
            "date": date.today()
        }
        serializer = CreateTransactionSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("amount", serializer.errors)

    def test_create_transaction_fails_with_invalid_type(self):
        data = {
            "amount": Decimal('100.00'),
            "category_id": 1,
            "type": "INVALID",
            "description": "Groceries",
            "date": date.today()
        }
        serializer = CreateTransactionSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("type", serializer.errors)

    def test_create_transaction_fails_with_missing_required_fields(self):
        data = {
            "description": "Groceries"
        }
        serializer = CreateTransactionSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("amount", serializer.errors)
        self.assertIn("category_id", serializer.errors)
        self.assertIn("type", serializer.errors)

    def test_create_transaction_with_optional_description(self):
        data = {
            "amount": Decimal('100.00'),
            "category_id": 1,
            "type": CategoryFields.INCOME,
            "description": "",
            "date": date.today()
        }
        serializer = CreateTransactionSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data.get("description"), "")
