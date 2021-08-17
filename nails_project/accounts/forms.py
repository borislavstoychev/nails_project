from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from nails_project.accounts.models import Profile
from nails_project.core.mixins import BootstrapFormMixin

UserModel = get_user_model()


class ProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'is_complete')


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("email",)


class SignInForm(BootstrapFormMixin, AuthenticationForm):

    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = f'Please enter a correct %(username)s and password.\n' \
                                               'Note that your profile must be activated, check your email!\n' \
                                               'Note that both fields may be case-sensitive.'
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

