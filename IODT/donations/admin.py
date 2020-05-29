from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from register.models import user, Doner, Recipient, People, Organization
from donations.models import RequireType
from django.contrib.auth.models import Permission

admin.site.register(Permission)

admin.site.register(user, UserAdmin)

admin.site.register(Doner)
admin.site.register(Recipient)
admin.site.register(People)
admin.site.register(Organization)

admin.site.register(RequireType)
