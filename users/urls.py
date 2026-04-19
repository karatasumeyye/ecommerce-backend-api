from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path("password-reset/request/",PasswordResetRequestView.as_view(),name="password-reset-request",),
    path("password-reset/confirm/",PasswordResetConfirmView.as_view(),name="password-reset-confirm",),
    path("email-verification/request/",EmailVerificationRequestView.as_view(),name="email-verification-request",),
    path("email-verification/confirm/",EmailVerificationConfirmView.as_view(),name="email-verification-confirm",),

]