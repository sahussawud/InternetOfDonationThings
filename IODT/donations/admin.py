from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from register.models import user

admin.site.register(user, UserAdmin)
