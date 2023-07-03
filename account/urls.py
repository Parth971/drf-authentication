from django.urls import path, include

from rest_framework.routers import DefaultRouter

from account.views import (
    LoginView, RegisterView, RefreshTokenView,
    LogoutView, VerifyEmailView, UserViewSet
)

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    # No AuthRequired
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),

    # This paths base name is used in utils
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify_user_email'),

    # AuthRequired
    path('token/', RefreshTokenView.as_view(), name='refresh_token'),
    path('logout/', LogoutView.as_view(), name='logout_user'),
    path('', include(router.urls)),
]
