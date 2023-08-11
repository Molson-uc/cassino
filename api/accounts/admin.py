from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_bank",
        "is_gamemaster",
    )
    fieldsets = UserAdmin.fieldsets + (
        (_("User type"), {"fields": ("is_bank", "is_gamemaster")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.
