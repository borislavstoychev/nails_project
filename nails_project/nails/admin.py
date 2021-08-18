from django.contrib import admin

# Register your models here.
from nails_project.nails.models import Nails, Like


@admin.register(Nails)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('type', 'feedback', 'description', 'image', 'user')
    list_filter = ('type', 'feedback', 'user')
    ordering = ('type',)


@admin.register(Like)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('nails', 'user')
    list_filter = ('nails', 'user' )
    ordering = ('user',)
