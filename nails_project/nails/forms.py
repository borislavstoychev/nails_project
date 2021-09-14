from django import forms

from nails_project.core.mixins import BootstrapFormMixin
from nails_project.nails.models import Feedback, Comment


class FeedbackForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = Feedback
        exclude = ('user', )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'is_required': True,
                },
            ),
        }
