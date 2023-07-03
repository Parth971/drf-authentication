from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView, TokenRefreshView

from account.constants import REGISTER_SUCCESS, LOGIN_SUCCESS, LOGOUT_SUCCESS, REFRESH_TOKEN_SUCCESS
from account.mixins import ExceptionHandlerMixin, VerifyEmailMixin, ModifyResponseMixin, EmailVerificationMixin
from account.models import User
from account.serializers import RegisterSerializer, LoginSerializer
from account.utils import send_email_verification_email


class RegisterView(ExceptionHandlerMixin, EmailVerificationMixin, ModifyResponseMixin, CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    message = REGISTER_SUCCESS

    def perform_create(self, serializer):
        super().perform_create(serializer)
        send_email_verification_email(
            serializer.instance,
            self.verification_email_txt_template,
            self.verification_email_html_template,
            self.verification_email_subject
        )

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return self.modify(response)


class LoginView(ExceptionHandlerMixin, ModifyResponseMixin, TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    message = LOGIN_SUCCESS

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return self.modify(response)


class LogoutView(ExceptionHandlerMixin, ModifyResponseMixin, TokenBlacklistView):
    message = LOGOUT_SUCCESS

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return self.modify(response)


class RefreshTokenView(ExceptionHandlerMixin, ModifyResponseMixin, TokenRefreshView):
    message = REFRESH_TOKEN_SUCCESS

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return self.modify(response)


class VerifyEmailView(ExceptionHandlerMixin, VerifyEmailMixin, APIView):
    permission_classes = (AllowAny,)

    def get(self, request, token, *args, **kwargs):
        return self.verify(token)
