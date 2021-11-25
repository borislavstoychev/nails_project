from django.contrib import admin

from nails_project.gallery.models import CommentImage, Gallery, LikeImage

# Register your models here.



@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('description', 'image',)
    list_filter = ('description', )
    ordering = ('image',)


@admin.register(LikeImage)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('image', 'user',)
    list_filter = ('image', 'user', )
    ordering = ('user',)


@admin.register(CommentImage)
class Commentdmin(admin.ModelAdmin):
    list_display = ('image', 'comment', 'user',)
    list_filter = ('image', 'user')
    ordering = ('user',)
