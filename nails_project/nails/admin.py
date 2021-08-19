from django.contrib import admin

# Register your models here.
from nails_project.nails.models import Feedback, Like


@admin.register(Feedback)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('type', 'feedback', 'description', 'image', 'user')
    list_filter = ('type', 'feedback', 'user')
    ordering = ('type',)


@admin.register(Like)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('feedback', 'user',)
    list_filter = ('feedback', 'user', )
    ordering = ('user',)
