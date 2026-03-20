from django.urls import path

from accounts.views import RegisterView, LoginView, ProfileView, ChangePasswordView, ForgotPasswordView, \
    ResetPasswordView, AuthValidateTokenView

urlpatterns = [

    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("profile", ProfileView.as_view()),
    path("change-password", ChangePasswordView.as_view()),
    path("forgot-password", ForgotPasswordView.as_view()),
    path("reset-password", ResetPasswordView.as_view()),
    path("reset-password", ResetPasswordView.as_view()),
    path('verify', AuthValidateTokenView.as_view()),
]
