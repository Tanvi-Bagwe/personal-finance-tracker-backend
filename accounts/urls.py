from django.urls import path

from accounts.views import RegisterView, LoginView, ProfileView, ChangePasswordView, AuthValidateTokenView, \
    RequestPasswordResetOTPView, ConfirmPasswordResetOTPView

urlpatterns = [

    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("profile", ProfileView.as_view()),
    path("change-password", ChangePasswordView.as_view()),
    path('verify', AuthValidateTokenView.as_view()),
    path('otp-request', RequestPasswordResetOTPView.as_view()),
    path('otp-confirm', ConfirmPasswordResetOTPView.as_view()),
]
