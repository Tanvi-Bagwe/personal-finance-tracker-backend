from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .constant import AuthFields
from .models import UserProfile


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_username(self, value):

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")

        return value

    def validate_email(self, value):

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")

        return value

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data[AuthFields.USERNAME],
            email=validated_data[AuthFields.EMAIL],
            password=validated_data[AuthFields.PASSWORD]
        )

        UserProfile.objects.create(user=user)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username=data[AuthFields.USERNAME],
            password=data[AuthFields.PASSWORD]
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data["user"] = user

        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8)
