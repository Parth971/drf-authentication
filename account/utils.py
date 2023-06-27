from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_mail(to, template, context):
    html_content = render_to_string(f'account/emails/{template}.html', context)
    msg = EmailMessage(context['subject'], html_content, to=[to])
    msg.send()


def send_email_verification_email(user):
    token = user.generate_activation_token()
    link = F"{settings.FRONT_END_DOMAIN}/auth/verify-email/{token}"
    context = {
        'subject': 'Email Verification',
        'uri': link,
    }
    send_mail(user.email, 'email_verification', context)


def get_model_object(model_class, query):
    """
    Retrieve a single object from the specified model class based on the provided query.

    Args:
        model_class (Model): The model class to retrieve the object from.
        query (dict): The query parameters used to filter the objects.

    Returns:
        Model: The retrieved object or None if not found.
    """
    return model_class.objects.filter(**query).first()
