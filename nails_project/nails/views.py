from django.shortcuts import render
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy
from nails_project.nails.forms import FeedbackForm, CommentForm
from nails_project.nails.models import Feedback, Like, Comment


class HomeView(generic.TemplateView):
    template_name = 'nails/index.html'


class AboutView(generic.TemplateView):
    template_name = 'nails/about.html'


class FeedbackListView(generic.ListView):
    model = Feedback
    template_name = 'nails/feedback_list.html'
    context_object_name = 'nails'


class FeedbackDetailsView(generic.DetailView):
    model = Feedback
    template_name = 'nails/feedback_details.html'
    context_object_name = 'nails'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nails = context[self.context_object_name]
        nails.likes_count = nails.like_set.count()
        context['is_owner'] = nails.user == self.request.user
        context['is_liked_by_user'] = nails.like_set.filter(user_id=self.request.user.id).exists()
        context['comments'] = nails.comment_set.all()
        return context


class FeedbackLikeView(auth_mixins.LoginRequiredMixin, generic.View):

    def get(self, request, **kwargs):
        user_profile = self.request.user
        feedback = Feedback.objects.get(pk=kwargs['pk'])
        like = feedback.like_set.filter(user_id=user_profile.id).first()
        if like:
            like.delete()
        else:
            like = Like(
                user=user_profile,
                feedback=feedback,
            )
            like.save()

        return redirect('feedback details', feedback.id)

    def dispatch(self, request, *args, **kwargs):
        user_profile = self.request.user
        nails = Feedback.objects.get(pk=kwargs['pk'])
        if nails.user_id == user_profile.id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class FeedbackCreateView(auth_mixins.LoginRequiredMixin, generic.CreateView):
    template_name = 'nails/feedback_create.html'
    model = Feedback
    form_class = FeedbackForm

    def get_success_url(self):
        url = reverse_lazy('feedback list')
        return url

    def form_valid(self, form):
        nails = form.save(commit=False)
        nails.user = self.request.user
        nails.save()
        return super().form_valid(form)


class FeedbackEditView(auth_mixins.LoginRequiredMixin, generic.UpdateView):
    template_name = 'nails/feedback_edit.html'
    model = Feedback
    form_class = FeedbackForm
    context_object_name = 'nails'

    def get_success_url(self):
        url = reverse_lazy('feedback details', kwargs={'pk': self.object.id})
        return url

    def dispatch(self, request, *args, **kwargs):
        nails = self.get_object()
        if nails.user_id != request.user.id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class FeedbackDeleteView(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    model = Feedback
    template_name = 'nails/feedback_delete.html'
    success_url = reverse_lazy('feedback list')

    def dispatch(self, request, *args, **kwargs):
        nails = self.get_object()
        if nails.user_id != request.user.id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class FeedbackCommentView(auth_mixins.LoginRequiredMixin, generic.FormView):
    form_class = CommentForm
    template_name = 'nails/feedback_comment.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.feedback = Feedback.objects.get(pk=self.kwargs['pk'])
        comment.save()
        return redirect('feedback details', self.kwargs['pk'])


class CommentUpdateView(auth_mixins.LoginRequiredMixin, generic.UpdateView):
    model = Comment
    context_object_name = 'comment'  # your own name for the list as a template variable
    form_class = CommentForm
    template_name = 'nails/feedback_comment_update.html'

    def get_success_url(self):
        url = reverse_lazy('feedback details', kwargs={'pk': self.object.feedback.id})
        return url

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user_id != request.user.id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    model = Comment
    template_name = 'nails/feedback_comment_delete.html'

    def get_success_url(self):
        url = reverse_lazy('feedback details', kwargs={'pk': self.object.feedback.id})
        return url

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user_id != request.user.id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
