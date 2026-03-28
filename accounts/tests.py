from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock

from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from accounts.serializers import LoginSerializer, ProfileSerializer, RequestOTPSerializer, ResetPasswordOTPSerializer


class LoginSerializerValidation(SimpleTestCase):

    @patch('accounts.serializers.authenticate')
    def test_successful_login_with_valid_credentials(self, mock_authenticate):
        mock_user = MagicMock(spec=User)
        mock_authenticate.return_value = mock_user

        data = {"username": "testuser", "password": "password123"}
        serializer = LoginSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["user"], mock_user)

    @patch('accounts.serializers.authenticate')
    def test_login_fails_with_invalid_credentials(self, mock_authenticate):
        mock_authenticate.return_value = None

        data = {"username": "testuser", "password": "wrongpassword"}
        serializer = LoginSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class ProfileSerializerValidation(SimpleTestCase):

    def test_profile_serializer_returns_user_fields(self):
        mock_user = MagicMock(spec=User)
        mock_user.id = 1
        mock_user.username = "testuser"
        mock_user.email = "test@example.com"

        serializer = ProfileSerializer(mock_user)

        self.assertEqual(serializer.data["id"], 1)
        self.assertEqual(serializer.data["username"], "testuser")
        self.assertEqual(serializer.data["email"], "test@example.com")


class RequestOTPSerializerValidation(SimpleTestCase):

    def test_request_otp_with_valid_email(self):
        data = {"email": "user@example.com"}
        serializer = RequestOTPSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_request_otp_fails_with_invalid_email(self):
        data = {"email": "invalid-email"}
        serializer = RequestOTPSerializer(data=data)

        self.assertFalse(serializer.is_valid())


class ResetPasswordOTPSerializerValidation(SimpleTestCase):

    def test_reset_password_otp_with_valid_data(self):
        data = {
            "email": "user@example.com",
            "otp": "123456",
            "new_password": "NewPassword123"
        }
        serializer = ResetPasswordOTPSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_reset_password_otp_fails_with_short_password(self):
        data = {
            "email": "user@example.com",
            "otp": "123456",
            "new_password": "short"
        }
        serializer = ResetPasswordOTPSerializer(data=data)

        self.assertFalse(serializer.is_valid())
