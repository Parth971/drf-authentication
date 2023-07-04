# drf-authentication

Integrate Authentication APIs with Django REST framework in the shortest way possible, with least efforts possible.

Package provides views, serializers, mixins, error handling and other handy add-ons.

You are expected to use [JWT](https://jwt.io/) for authentication purpose and smtp to send emails.

[![image search api](https://img.shields.io/badge/pypi-v0.0.1-orange)](https://pypi.python.org/pypi/django-elasticsearch-dsl-drf) [![image search api](https://img.shields.io/badge/python-3.10%20%7C%203.9-blue)](https://pypi.python.org/pypi/django-elasticsearch-dsl-drf) [![image search api](https://img.shields.io/badge/test-passing-darkGreen)](https://pypi.python.org/pypi/django-elasticsearch-dsl-drf)  [![image search api](https://img.shields.io/badge/test-passing-darkGreen)](https://pypi.python.org/pypi/django-elasticsearch-dsl-drf)  [![image search api](https://img.shields.io/badge/licence-MIT-blue)](https://pypi.python.org/pypi/django-elasticsearch-dsl-drf)  [![image search api](https://img.shields.io/badge/coverage-98%25-yellow)](https://pypi.python.org/pypi/django-elasticsearch-dsl-drf)

## Documentation

Documentation is available on [Read the Docs.](link_to_docs)

Make sure to read FAQ.

## Prerequisites

- Django 4.2.2
- Python 3.10
- djangorestframework 3.14.0

## Main features and highlights

- Best built-in library for authentication purpose
- No need to create basic APIs like login, register, etc. its all included


### Installation

1. Install latest stable version from PyPI:
    
        pip install drf-authentication    

2. Add `rest_framework`, `rest_framework_simplejwt` and `drf_authentication` to INSTALLED_APPS:

        INSTALLED_APPS = (
            # ...
            # REST framework
            'rest_framework',
        
            # Django REST framework SimpleJWT integration
            'rest_framework_simplejwt',
        
            # Django REST framework Authentication integration (this package)
            'drf_authentication',
            # ...
        )
        
3. Django Settings
        
        REST_FRAMEWORK = {
            'DEFAULT_AUTHENTICATION_CLASSES': [
                'rest_framework_simplejwt.authentication.JWTAuthentication',
                # ...
            ],
            'DEFAULT_PERMISSION_CLASSES': (
                'rest_framework.permissions.IsAuthenticated',
                # ...
            )
        }
        
        AUTH_USER_MODEL = 'account.User'

        EMAIL_USE_TLS = True
        EMAIL_HOST = 'smtp.gmail.com'
        EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
        EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
        EMAIL_PORT = 587
        
        # Optional
        VERIFICATION_EMAIL_HTML_TEMPLATE = 'account/emails/email_verification.html'
        VERIFICATION_EMAIL_TXT_TEMPLATE = 'account/emails/email_verification.txt'
        VERIFICATION_EMAIL_SUBJECT = 'Account Verification'


## License

[MIT](https://github.com/Parth971/drf-authentication/blob/main/Licence)

## Support

For any issues contact me at the e-mail given in the [Author](https://github.com/Parth971/drf-authentication/#author) section.

## Author

Parth Desai <[desaiparth971@gmail.com](mailto:desaiparth971@gmail.com)>
