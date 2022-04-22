from tabnanny import verbose
from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class UserInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Users'


class customeUser (UserAdmin):
    inlines = (UserInLine,)


admin.site.unregister(User)
admin.site.register(User, customeUser)
