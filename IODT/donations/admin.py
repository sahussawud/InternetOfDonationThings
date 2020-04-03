from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from register.models import user, Doner, Recipient, People, Organization

admin.site.register(user, UserAdmin)
admin.site.register(Doner)
admin.site.register(Recipient)
admin.site.register(People)
admin.site.register(Organization)
