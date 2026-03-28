from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from core.constants import ResponseMessages
from .constant import AuthFields
from .models import UserProfile
from rest_framework.exceptions import ValidationError

class RegisterSerializer(serializers.Serializer):
    # Serializer for user registration
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_username(self, value):
        # Check if username already exists
        if User.objects.filter(username=value).exists():
            raise ValidationError(ResponseMessages.USERNAME_EXISTS)
        return value

    def validate_email(self, value):
        # Check if email already exists
        if User.objects.filter(email=value).exists():
            raise ValidationError(ResponseMessages.EMAIL_EXISTS)
        return value

    def create(self, validated_data):
        # Create new user and profile
        user = User.objects.create_user(
            username=validated_data[AuthFields.USERNAME],
            email=validated_data[AuthFields.EMAIL],
            password=validated_data[AuthFields.PASSWORD]
        )
        UserProfile.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    # Serializer for user login
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        # Authenticate user with provided credentials
        user = authenticate(
            username=data[AuthFields.USERNAME],
            password=data[AuthFields.PASSWORD]
        )

        if not user:
            raise ValidationError(ResponseMessages.INVALID_CREDENTIALS)

        data["user"] = user
        return data


class ProfileSerializer(serializers.ModelSerializer):
    # Serializer for user profile data
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class RequestOTPSerializer(serializers.Serializer):
    # Serializer for requesting OTP
    email = serializers.EmailField()


class ResetPasswordOTPSerializer(serializers.Serializer):
    # Serializer for resetting password with OTP
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8)
