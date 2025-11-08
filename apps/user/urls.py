from django.urls import path, include
from .views import (
    RegisterView, VerifyOTPView, ResendOTPView, LoginView,
    ResetPasswordView, ResetPasswordConfirmView,
    UserMeView, UserUpdateProfileView, UserDeleteAccountView,
     AvatarView, GoogleLoginView
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/verify-otp/", VerifyOTPView.as_view()),
    path("auth/resend-otp/", ResendOTPView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("auth/reset-password/", ResetPasswordView.as_view()),
    path("auth/reset-password-confirm/", ResetPasswordConfirmView.as_view()),

    path("me/", UserMeView.as_view()),
    path("update-profile/", UserUpdateProfileView.as_view()),
    path("delete-account/", UserDeleteAccountView.as_view()),

    path("avatar/", AvatarView.as_view()),

    path("auth/google/", GoogleLoginView.as_view()),
]
