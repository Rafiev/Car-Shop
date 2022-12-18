from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from applications.account.views import RegisterAPIView, ActivationAPIView, ForgotPasswordAPIView, \
    ForgotPasswordCompleteAPIView, ChangedPasswordAPIView, ChangedEmailAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('activate/<uuid:activation_code>', ActivationAPIView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('forgot_password/', ForgotPasswordAPIView.as_view()),
    path('forgot_password_complete/', ForgotPasswordCompleteAPIView.as_view()),
    path('changed_password/', ChangedPasswordAPIView.as_view()),
    path('changed_email/', ChangedEmailAPIView.as_view())
]