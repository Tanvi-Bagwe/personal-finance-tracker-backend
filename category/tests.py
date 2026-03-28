from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock

from category.serializers import CreateCategorySerializer, CategorySerializer
from category.constant import CategoryFields


class CreateCategorySerializerValidation(SimpleTestCase):

    def test_create_category_with_valid_data(self):
        data = {
            "name": "Groceries",
            "type": CategoryFields.EXPENSE
        }
        serializer = CreateCategorySerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], "Groceries")
        self.assertEqual(serializer.validated_data["type"], CategoryFields.EXPENSE)

    def test_create_category_fails_with_missing_name(self):
        data = {
            "type": CategoryFields.EXPENSE
        }
        serializer = CreateCategorySerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_create_category_fails_with_invalid_type(self):
        data = {
            "name": "Groceries",
            "type": "INVALID"
        }
        serializer = CreateCategorySerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("type", serializer.errors)


class CategorySerializerValidation(SimpleTestCase):

    def test_category_serializer_returns_all_fields(self):
        mock_category = MagicMock()
        mock_category.id = 1
        mock_category.name = "Groceries"
        mock_category.type = CategoryFields.EXPENSE

        serializer = CategorySerializer(mock_category)

        self.assertEqual(serializer.data["id"], 1)
        self.assertEqual(serializer.data["name"], "Groceries")
        self.assertEqual(serializer.data["type"], CategoryFields.EXPENSE)
