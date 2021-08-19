from django import forms

from nails_project.core.mixins import BootstrapFormMixin
from nails_project.nails.models import Feedback


class FeedbackForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = Feedback
        exclude = ('user', )
