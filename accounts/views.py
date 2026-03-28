import random

from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, ValidationError, APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from core.constants import ResponseMessages, ResponseFields
from core.settings import EMAIL_HOST_USER
from .constant import AuthFields
from .models import PasswordResetOTP
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, RequestOTPSerializer, \
    ResetPasswordOTPSerializer


class RegisterView(APIView):
    """Handle user registration"""

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({
            ResponseFields.MESSAGE: ResponseMessages.REGISTER_SUCCESS,
        })


class LoginView(APIView):
    """Handle user login and generate tokens"""

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response({
            ResponseFields.MESSAGE: ResponseMessages.LOGIN_SUCCESS,
            AuthFields.ACCESS: str(refresh.access_token),
            AuthFields.REFRESH: str(refresh)
        })


class ProfileView(APIView):
    """Get authenticated user profile"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)

        return Response(serializer.data)


class ChangePasswordView(APIView):
    """Change password for authenticated user"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        old_password = request.data.get(AuthFields.OLD_PASSWORD)
        new_password = request.data.get(AuthFields.NEW_PASSWORD)

        # Verify old password before changing
        if not user.check_password(old_password):
            raise ValidationError(ResponseMessages.INCORRECT_PASSWORD)

        user.set_password(new_password)
        user.save()

        return Response({ResponseFields.MESSAGE: ResponseMessages.PASSWORD_UPDATE_SUCCESS})


class AuthValidateTokenView(APIView):
    """Validate and refresh JWT tokens"""
    def post(self, request):
        access_token_str = request.data.get(AuthFields.ACCESS)
        refresh_token_str = request.data.get(AuthFields.REFRESH)

        if not access_token_str:
            raise ValidationError(ResponseMessages.ACCESS_TOKEN_REQUIRED)

        try:
            # Check if access token is valid
            AccessToken(access_token_str)
            return Response({
                ResponseFields.MESSAGE: ResponseMessages.ACCESS_TOKEN_VALID
            })

        except Exception:
            # If access token expired, try to refresh it
            if not refresh_token_str:
                raise AuthenticationFailed(ResponseMessages.SESSION_EXPIRED_OR_INVALID)

            try:
                refresh = RefreshToken(refresh_token_str)
                return Response({
                    ResponseFields.MESSAGE: ResponseMessages.ACCESS_TOKEN_REFRESHED,
                    AuthFields.ACCESS: str(refresh.access_token),
                })

            except Exception:
                raise AuthenticationFailed(ResponseMessages.SESSION_EXPIRED)


class RequestPasswordResetOTPView(APIView):
    """Generate and send OTP for password reset"""
    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data[AuthFields.EMAIL]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if email exists or not
            return Response({ResponseFields.MESSAGE: ResponseMessages.OTP_SENT})

        # Generate 6-digit OTP
        otp_code = str(random.randint(100000, 999999))

        # Delete old OTPs and create new one
        PasswordResetOTP.objects.filter(user=user).delete()
        PasswordResetOTP.objects.create(user=user, otp=otp_code)

        context = {'otp_code': otp_code}
        html_content = render_to_string('emails/otp_reset.html', context)
        text_content = strip_tags(html_content)

        try:
            email_message = EmailMultiAlternatives(
                subject="🔒 Your Password Reset Code",
                body=text_content,
                from_email=EMAIL_HOST_USER,
                to=[email],
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()


        except Exception as e:
            print(f"SMTP Error: {e}")
            raise APIException(ResponseMessages.OTP_SEND_FAILED)

        return Response({ResponseFields.MESSAGE: ResponseMessages.OTP_SENT})


class ConfirmPasswordResetOTPView(APIView):
    """Reset password using OTP"""
    def post(self, request):
        serializer = ResetPasswordOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data[AuthFields.EMAIL]
        otp = serializer.validated_data[AuthFields.OTP]
        new_password = serializer.validated_data[AuthFields.NEW_PASSWORD]

        # Get user and OTP record
        try:
            user = User.objects.get(email=email)
            otp_record = PasswordResetOTP.objects.filter(user=user, otp=otp).latest('created_at')
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            raise ValidationError(ResponseMessages.INVALID_EMAIL_OTP)

        # Check if OTP has expired
        if otp_record.is_expired():
            raise ValidationError(ResponseMessages.OTP_EXPIRED)

        user.set_password(new_password)
        user.save()

        # Delete used OTP
        PasswordResetOTP.objects.filter(user=user).delete()

        return Response({
            ResponseFields.MESSAGE: ResponseMessages.PASSWORD_RESET_SUCCESSFUL
        })
