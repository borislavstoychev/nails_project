from django.contrib import admin

# Register your models here.


from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from nails_project.accounts.models import Profile

UserModel = get_user_model()


@admin.register(UserModel)
class NailsUserAdmin(UserAdmin):
    list_display = ('email', 'is_staff', "is_active")
    list_filter = ('is_staff', 'is_superuser', 'groups', "is_active")
    ordering = ('date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('date_joined',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    user field should not be changed
    """
    readonly_fields = ('user',)




