from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse


def send_mail(to, txt_template, html_template, context):
    txt_body = render_to_string(txt_template, context)
    html_body = render_to_string(html_template, context)

    msg = EmailMultiAlternatives(context['subject'], txt_body, to=[to])
    msg.attach_alternative(html_body, "text/html")
    msg.send()


def send_email_verification_email(user, txt_template, html_template, subject):
    token = user.generate_activation_token()
    url = reverse('verify_user_email', args=[token])
    context = {
        'subject': subject,
        'uri': f"{settings.FRONT_END_DOMAIN}{url}",
    }
    send_mail(user.email, txt_template, html_template, context)
