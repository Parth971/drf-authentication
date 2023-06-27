from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView, )
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView, TokenRefreshView

from account.constants import (
    REGISTER_SUCCESS, LOGIN_SUCCESS, LOGOUT_SUCCESS,
    REFRESH_TOKEN_SUCCESS, INVALID_TOKEN, EMAIL_VERIFIED_SUCCESS
)
from account.models import User, ActivateUserToken
from account.serializers import (
    RegisterSerializer, LoginSerializer
)
from account.utils import get_model_object


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data = {
            'message': REGISTER_SUCCESS,
            'data': response.data
        }
        return response


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        email = request.data['email']
        user = get_model_object(User, query={'email': email})

        response.data = {
            'message': LOGIN_SUCCESS,
            'data': {
                **response.data,
                "is_admin": user.is_staff
            }
        }

        return response


class LogoutView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data = {
            'message': LOGOUT_SUCCESS,
            'data': response.data
        }
        return response


class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data = {
            'message': REFRESH_TOKEN_SUCCESS,
            'data': response.data
        }
        return response


class VerifyEmailView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, token):
        """
        Get request to check token and activate user.
        :return: status code 200 for success and 404 for invalid token.
        """
        activate_user_token: ActivateUserToken = get_model_object(ActivateUserToken, query={'token': token})
        if activate_user_token is None:
            raise ValidationError({'message': INVALID_TOKEN})

        activate_user_token.user.activate()
        activate_user_token.delete_token()
        return Response(data={'message': EMAIL_VERIFIED_SUCCESS}, status=status.HTTP_200_OK)
