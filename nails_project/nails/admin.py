from django.contrib import admin

# Register your models here.
from nails_project.nails.models import Comment, Feedback, Like


@admin.register(Feedback)
class FeadbackAdmin(admin.ModelAdmin):
    list_display = ('type', 'feedback', 'description', 'image', 'user')
    list_filter = ('type', 'feedback', 'user')
    ordering = ('type',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('feedback', 'user',)
    list_filter = ('feedback', 'user', )
    ordering = ('user',)


@admin.register(Comment)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('feedback', 'comment', 'user',)
    list_filter = ('feedback', 'user', )
    ordering = ('user',)
