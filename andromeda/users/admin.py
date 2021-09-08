"""Admin de usuarios."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Modelos
from andromeda.users.models import User, Profile


class CustomUserAdmin(UserAdmin):
    """Modelo del admin de usuarios."""
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'is_client',
        'is_admin',
        'is_employee',
        'is_assistant',
        'is_active',
        'is_verified',
    )
    list_filter = (
        'is_client',
        'is_admin',
        'is_employee',
        'is_assistant',
        'created',
        'modified'
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Modelo del admin de perfiles de usuarios."""
    list_display = ('user', 'picture',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')


admin.site.register(User, CustomUserAdmin)
