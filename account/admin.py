from django.contrib import admin

from account.models import User, ActivateUserToken

admin.site.register([User, ActivateUserToken])
