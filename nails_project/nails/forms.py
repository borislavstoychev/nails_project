from django import forms

from nails_project.core.mixins import BootstrapFormMixin
from nails_project.nails.models import Nails


class NailsForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = Nails
        exclude = ('user', )
