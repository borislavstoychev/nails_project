from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import mixins as auth_mixins

from nails_project.gallery.forms import GalleryForm, GalleryCommentForm
from nails_project.gallery.models import Gallery, LikeImage, CommentImage


class GalleryCreateView(auth_mixins.LoginRequiredMixin, generic.FormView):
    form_class = GalleryForm
    template_name = 'gallery/image_create.html'

    def form_valid(self, form):
        image = form.save(commit=False)
        image.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = Gallery.objects.all()
        context['images'] = images
        return context

    def get_success_url(self):
        url = reverse_lazy('add image')
        return url

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class GalleryListView(generic.ListView):
    model = Gallery
    template_name = 'gallery/gallery.html'
    context_object_name = 'images'


class GalleryDetailsView(generic.DetailView):
    model = Gallery
    template_name = 'gallery/image_details.html'
    context_object_name = 'image'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image = context[self.context_object_name]
        image.likes_count = image.likeimage_set.count()
        context['is_liked_by_user'] = image.likeimage_set.filter(user_id=self.request.user.id).exists()
        context['comments'] = image.commentimage_set.all()
        return context


class GalleryLikeView(auth_mixins.LoginRequiredMixin, generic.View):

    def get(self, request, **kwargs):
        user_profile = self.request.user
        image = Gallery.objects.get(pk=kwargs['pk'])
        like = image.likeimage_set.filter(user_id=user_profile.id).first()
        if like:
            like.delete()
        else:
            like = LikeImage(
                user=user_profile,
                image=image,
            )
            like.save()

        return redirect('image details', image.id)


class GalleryDeleteView(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    model = Gallery
    template_name = 'gallery/image_delete.html'
    success_url = reverse_lazy('add image')


class GalleryCommentView(auth_mixins.LoginRequiredMixin, generic.FormView):
    form_class = GalleryCommentForm
    template_name = 'gallery/image_comment.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.image = Gallery.objects.get(pk=self.kwargs['pk'])
        comment.save()
        return redirect('image details', self.kwargs['pk'])


class CommentUpdateView(auth_mixins.LoginRequiredMixin, generic.UpdateView):
    model = CommentImage
    context_object_name = 'comment'  # your own name for the list as a template variable
    form_class = GalleryCommentForm
    template_name = 'gallery/image_comment_update.html'

    def get_success_url(self):
        url = reverse_lazy('image details', kwargs={'pk': self.object.image.id})
        return url

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user_id != request.user.id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    model = CommentImage
    template_name = 'nails/feedback_comment_delete.html'

    def get_success_url(self):
        url = reverse_lazy('image details', kwargs={'pk': self.object.image.id})
        return url

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user_id != request.user.id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


