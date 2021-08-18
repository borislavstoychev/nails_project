from django.shortcuts import render
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy
from nails_project.nails.forms import NailsForm
from nails_project.nails.models import Nails, Like


class HomeView(generic.TemplateView):
    template_name = 'nails/index.html'


class AboutView(generic.TemplateView):
    template_name = 'nails/about.html'


class NailsListView(generic.ListView):
    model = Nails
    template_name = 'nails/nails_list.html'
    context_object_name = 'nails'


class NailsDetailsView(generic.DetailView):
    model = Nails
    template_name = 'nails/nails_details.html'
    context_object_name = 'nails'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nails = context[self.context_object_name]
        nails.likes_count = nails.like_set.count()
        context['is_owner'] = nails.user == self.request.user
        context['is_liked_by_user'] = nails.like_set.filter(user_id=self.request.user.id).exists()
        return context


class NailsLikeView(auth_mixins.LoginRequiredMixin, generic.View):

    def get(self, request, **kwargs):
        user_profile = self.request.user
        nails = Nails.objects.get(pk=kwargs['pk'])
        like = nails.like_set.filter(user_id=user_profile.id).first()
        if like:
            like.delete()
        else:
            like = Like(
                user=user_profile,
                nails=nails,
            )
            like.save()

        return redirect('nails details', nails.id)

    def dispatch(self, request, *args, **kwargs):
        user_profile = self.request.user
        nails = Nails.objects.get(pk=kwargs['pk'])
        if nails.user_id == user_profile.id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class NailsCreateView(auth_mixins.LoginRequiredMixin, generic.CreateView):
    template_name = 'nails/nails_create.html'
    model = Nails
    form_class = NailsForm

    def get_success_url(self):
        url = reverse_lazy('list nails')
        return url

    def form_valid(self, form):
        nails = form.save(commit=False)
        nails.user = self.request.user
        nails.save()
        return super().form_valid(form)


class NailsEditView(auth_mixins.LoginRequiredMixin, generic.UpdateView):
    template_name = 'nails/nails_edit.html'
    model = Nails
    form_class = NailsForm

    def get_success_url(self):
        url = reverse_lazy('list nails')
        return url

    def dispatch(self, request, *args, **kwargs):
        nails = self.get_object()
        if nails.user_id != request.user.id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class NailsDeleteView(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    model = Nails
    template_name = 'nails/nails_delete.html'
    success_url = reverse_lazy('list nails')

    def dispatch(self, request, *args, **kwargs):
        nails = self.get_object()
        if nails.user_id != request.user.id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
