from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer

from account.models import User

from account.constants import (
    PASSWORD_HELP_TEXT, EMAIL_NOT_UNIQUE, EMAIL_REQUIRED_ERROR,
    PASSWORD_REQUIRED_ERROR, FIRST_NAME_REQUIRED_ERROR, LAST_NAME_REQUIRED_ERROR,
    MOBILE_NUMBER_REQUIRED_ERROR, COMPANY_NAME_REQUIRED_ERROR, JOB_TITLE_REQUIRED_ERROR,
    LOGIN_FAILED
)

from account.utils import send_email_verification_email, get_model_object
from account.validators import validate_password, validate_first_name, validate_last_name, validate_mobile_number


class LoginSerializer(TokenObtainPairSerializer, TokenObtainSerializer):
    default_error_messages = {"no_active_account": LOGIN_FAILED}

    @classmethod
    def get_token(cls, user):
        token = super(LoginSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        return token

    def validate(self, attrs):
        user = get_model_object(User, query={'email': attrs[self.username_field]})

        if user and not user.is_active:
            raise serializers.ValidationError({'email': 'Email is not verified'})

        return super().validate(attrs)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message=EMAIL_NOT_UNIQUE)],
        error_messages={'required': EMAIL_REQUIRED_ERROR, 'blank': EMAIL_REQUIRED_ERROR}
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text=PASSWORD_HELP_TEXT,
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
        """
        This function will create user instance and send email regarding email verification.
        :rtype: User object
        """
        user = User.objects.create_user(**validated_data, is_active=False)
        send_email_verification_email(user)
        return user
