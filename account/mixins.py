from django.conf import settings
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from account.constants import VERIFICATION_EMAIL_SUBJECT
from account.models import ActivateUserToken


class ExceptionHandlerMixin:

    def get_exception_handler(self):
        return self.custom_exception_handler

    @staticmethod
    def custom_exception_handler(exc, context):
        # Call REST framework's default exception handler first,
        # to get the standard error response.
        response = exception_handler(exc, context)
        if response and issubclass(response.data.__class__, dict):
            if response.data.get('detail'):
                response.data['message'] = response.data.pop('detail')
            else:
                response.data = {
                    field: messages[0] if isinstance(messages, list) else messages for field, messages in response.data.items()
                }

        return response


class VerifyEmailMixin:
    invalid_token_message = 'Token Invalid!'
    email_verified_message = "Email verification successful"

    def verify(self, token):
        if activate_user_token := ActivateUserToken.objects.filter(token=token).first():
            activate_user_token.user.activate()
            activate_user_token.delete_token()
            return Response(
                data={'message': self.email_verified_message}, status=status.HTTP_200_OK
            )

        raise ValidationError({'message': self.invalid_token_message})


class EmailVerificationMixin:
    html_template = 'account/emails/email_verification.html'
    txt_template = 'account/emails/email_verification.txt'
    subject = VERIFICATION_EMAIL_SUBJECT

    @property
    def verification_email_html_template(self):
        template = (
            settings.VERIFICATION_EMAIL_HTML_TEMPLATE
            if hasattr(settings, 'VERIFICATION_EMAIL_HTML_TEMPLATE')
            else self.html_template
        )

        try:
            get_template(template)
        except TemplateDoesNotExist as e:
            error_message = f"VERIFICATION_EMAIL_HTML_TEMPLATE={template} is not valid template path"
            raise TemplateDoesNotExist(error_message) from e
        return template

    @property
    def verification_email_txt_template(self):
        template = (
            settings.VERIFICATION_EMAIL_TXT_TEMPLATE
            if hasattr(settings, 'VERIFICATION_EMAIL_TXT_TEMPLATE')
            else self.txt_template
        )

        try:
            get_template(template)
        except TemplateDoesNotExist as e:
            error_message = f"VERIFICATION_EMAIL_TXT_TEMPLATE={template} is not valid template path"
            raise TemplateDoesNotExist(error_message) from e
        return template

    @property
    def verification_email_subject(self):
        return (
            settings.VERIFICATION_EMAIL_SUBJECT
            if hasattr(settings, 'VERIFICATION_EMAIL_SUBJECT')
            else self.subject
        )


class ModifyResponseMixin:
    message = None

    def modify(self, response):
        response.data = {
            'message': self.message,
            'data': response.data
        }
        return response
