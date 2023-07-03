from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer

from account.constants import (
    EMAIL_NOT_UNIQUE, EMAIL_REQUIRED_ERROR, LOGIN_FAILED, EMAIL_UNVERIFIED,
    PASSWORD_REQUIRED_ERROR, FIRST_NAME_REQUIRED_ERROR, LAST_NAME_REQUIRED_ERROR
)
from account.models import User
from account.validators import validate_password, validate_first_name, validate_last_name


class LoginSerializer(TokenObtainPairSerializer, TokenObtainSerializer):
    default_error_messages = {
        "no_active_account": LOGIN_FAILED,
        "not_verified": EMAIL_UNVERIFIED,
    }

    @classmethod
    def get_token(cls, user):
        token = super(LoginSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        return token

    def validate(self, attrs):
        user = User.objects.filter(email=attrs[self.username_field]).first()

        if user and not user.is_active:
            raise serializers.ValidationError({'email': self.default_error_messages.get('not_verified')})

        return super().validate(attrs)

    @property
    def validated_data(self):
        validated_data = super().validated_data
        validated_data['admin'] = self.user.is_staff
        return validated_data


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message=EMAIL_NOT_UNIQUE)],
        error_messages={'required': EMAIL_REQUIRED_ERROR, 'blank': EMAIL_REQUIRED_ERROR}
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        error_messages={'required': PASSWORD_REQUIRED_ERROR, 'blank': PASSWORD_REQUIRED_ERROR}
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'first_name': {
                'required': True,
                'allow_blank': False,
                'validators': [validate_first_name],
                'error_messages': {
                    'required': FIRST_NAME_REQUIRED_ERROR,
                    'blank': FIRST_NAME_REQUIRED_ERROR
                }
            },
            'last_name': {
                'required': True,
                'allow_blank': False,
                'validators': [validate_last_name],
                'error_messages': {
                    'required': LAST_NAME_REQUIRED_ERROR,
                    'blank': LAST_NAME_REQUIRED_ERROR
                }
            }
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data, is_active=False)
