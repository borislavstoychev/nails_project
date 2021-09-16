from django import forms

from nails_project.core.mixins import BootstrapFormMixin
from nails_project.gallery.models import Gallery, CommentImage


class GalleryForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = Gallery
        fields = "__all__"


class GalleryCommentForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = CommentImage
        fields = ('comment', )
