import random

from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from core.settings import EMAIL_HOST_USER
from .constant import AuthFields
from .models import PasswordResetOTP
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, RequestOTPSerializer, \
    ResetPasswordOTPSerializer


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                AuthFields.MESSAGE: "User registered successfully"
            })

        return Response({
            "errors": serializer.errors
        }, status=400)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            refresh = RefreshToken.for_user(user)

            return Response({
                AuthFields.ACCESS: str(refresh.access_token),
                AuthFields.REFRESH: str(refresh)
            })

        return Response(serializer.errors, status=400)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)

        return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        old_password = request.data.get(AuthFields.OLD_PASSWORD)
        new_password = request.data.get(AuthFields.NEW_PASSWORD)

        if not user.check_password(old_password):
            return Response({AuthFields.ERROR: "Incorrect password"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({AuthFields.MESSAGE: "Password updated"})


class AuthValidateTokenView(APIView):
    def post(self, request):
        access_token_str = request.data.get(AuthFields.ACCESS)
        refresh_token_str = request.data.get(AuthFields.REFRESH)

        if not access_token_str:
            return Response({"error": "Access token required"}, status=400)

        # 1. Try validating the Access Token
        try:
            AccessToken(access_token_str)
            return Response({"status": "valid", "message": "Access token is valid"}, status=200)

        except Exception:
            # This catches BOTH InvalidToken AND low-level decoding errors (the 500 culprits)

            # 2. Access is dead/malformed. Try the Refresh Token.
            if not refresh_token_str:
                return Response({"error": "Access invalid/expired and no refresh provided"}, status=401)

            try:
                refresh = RefreshToken(refresh_token_str)
                # 3. Success!
                return Response({
                    "status": "refreshed",
                    AuthFields.ACCESS: str(refresh.access_token),
                }, status=200)

            except Exception:
                # 4. Refresh token is also malformed or expired
                return Response({"error": "Session expired, please login again"}, status=401)


class RequestPasswordResetOTPView(APIView):
    def post(self, request):
        # 1. Keep your Serializer Validation
        serializer = RequestOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data[AuthFields.EMAIL]

        # 2. Keep your Security-First User Lookup
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Generic response to prevent "Email Harvesting"
            return Response({AuthFields.MESSAGE: "If an account exists, an OTP has been sent."})

        # 3. Generate OTP
        otp_code = str(random.randint(100000, 999999))

        # 4. Database cleanup and creation
        PasswordResetOTP.objects.filter(user=user).delete()
        PasswordResetOTP.objects.create(user=user, otp=otp_code)

        # 5. Professional HTML Email Logic
        context = {'otp_code': otp_code}
        html_content = render_to_string('emails/otp_reset.html', context)
        text_content = strip_tags(html_content)  # Fallback for plain-text clients

        try:
            email_message = EmailMultiAlternatives(
                subject="🔒 Your Password Reset Code",
                body=text_content,
                from_email=EMAIL_HOST_USER,
                to=[email],
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

            # Keep your debug logs for dev
            print(f"DEBUG: OTP {otp_code} sent to {email}")

        except Exception as e:
            print(f"SMTP Error: {e}")
            # If email fails, we should let the user know something went wrong internally
            return Response({AuthFields.ERROR: "Failed to send email. Please try again later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({AuthFields.MESSAGE: "OTP sent successfully."})


class ConfirmPasswordResetOTPView(APIView):
    def post(self, request):
        serializer = ResetPasswordOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data[AuthFields.EMAIL]
        otp = serializer.validated_data[AuthFields.OTP]
        new_password = serializer.validated_data[AuthFields.NEW_PASSWORD]

        try:
            user = User.objects.get(email=email)
            otp_record = PasswordResetOTP.objects.filter(user=user, otp=otp).latest('created_at')
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            return Response({AuthFields.ERROR: "Invalid OTP or Email"}, status=status.HTTP_400_BAD_REQUEST)

        if otp_record.is_expired():
            return Response({AuthFields.ERROR: "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

        # Update Password
        user.set_password(new_password)
        user.save()

        # Cleanup
        PasswordResetOTP.objects.filter(user=user).delete()

        return Response({AuthFields.MESSAGE: "Password reset successful."})
