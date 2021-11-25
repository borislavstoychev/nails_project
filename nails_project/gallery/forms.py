from django import forms

from nails_project.core.mixins import BootstrapFormMixin
from nails_project.gallery.models import Gallery, CommentImage


class GalleryForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = Gallery
        fields = "__all__"
        widgets = {
            'image': forms.FileInput(
                attrs={
                    'type': 'file',
                    'class': 'form-control',
                    'required': '',
                    'name': 'image',
                    'id': 'id_image',
                    'multiple': ''
                },
            ),
        }


class GalleryCommentForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = CommentImage
        fields = ('comment', )
