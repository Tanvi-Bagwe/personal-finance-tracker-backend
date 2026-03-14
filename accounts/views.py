from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .constant import AuthFields
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from .tokens import password_reset_token


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


class ForgotPasswordView(APIView):

    def post(self, request):

        email = request.data.get(AuthFields.EMAIL)

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return Response({AuthFields.ERROR: "User not found"}, status=404)

        token = password_reset_token.make_token(user)

        return Response({
            AuthFields.USER_ID: user.id,
            AuthFields.TOKEN: token
        })


class ResetPasswordView(APIView):

    def post(self, request):

        user_id = request.data.get(AuthFields.USER_ID)
        token = request.data.get(AuthFields.TOKEN)
        new_password = request.data.get(AuthFields.NEW_PASSWORD)

        user = User.objects.get(id=user_id)

        if not password_reset_token.check_token(user, token):
            return Response({AuthFields.ERROR: "Invalid token"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({AuthFields.MESSAGE: "Password reset successful"})