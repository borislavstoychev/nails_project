from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.contrib.auth import mixins as auth_mixins
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.views import View
from nails_project import settings
from nails_project.accounts.forms import SignUpForm, SignInForm, ProfileForm
from nails_project.accounts.models import Profile
# Django registration with confirmation email
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.http import HttpResponse
from nails_project.core.email_threading import EmailThread

UserModel = get_user_model()


class SignUpView(generic.CreateView):
    template_name = 'account/auth/sign_up.html'
    model = UserModel
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account.'
        message = render_to_string('account/auth/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        EmailThread(email).start()
        return render(self.request, 'account/auth/inactive_profile.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('profile details', user.id)
    else:
        return HttpResponse('Activation link is invalid!')


class SignInView(LoginView):
    template_name = 'account/auth/sign_in.html'
    form_class = SignInForm

    def get_success_url(self):
        return reverse('home')


class SignOutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)


class ProfileUpdateView(auth_mixins.LoginRequiredMixin, generic.UpdateView):
    model = Profile
    context_object_name = 'profile'  # your own name for the list as a template variable
    form_class = ProfileForm
    template_name = 'account/profiles/profile_details.html'

    def get_success_url(self):
        url = reverse_lazy('profile details', kwargs={'pk': self.request.user.id})
        return url

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the nails
        context['nails'] = self.get_object().user.nails_set.all()
        return context


class ProfileDeleteView(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    model = UserModel
    template_name = 'account/profiles/profile_delete.html'
    success_url = reverse_lazy('sign up user')

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.id != request.user.id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
