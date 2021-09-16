from django.urls import path

from nails_project.gallery import views

urlpatterns = [
    path('image-add/', views.GalleryCreateView.as_view(), name='add image'),
    path('image-delete/<int:pk>/', views.GalleryDeleteView.as_view(), name='delete image'),
    path('', views.GalleryListView.as_view(), name='gallery'),
    path('image-details/<int:pk>/', views.GalleryDetailsView.as_view(), name='image details'),
    path('image-like/<int:pk>/', views.GalleryLikeView.as_view(), name='image like'),
    path('comment/<int:pk>/', views.GalleryCommentView.as_view(), name='comment image'),
    path('comment-update/<int:pk>', views.CommentUpdateView.as_view(), name='update comment'),
    path('comment-delete/<int:pk>', views.CommentDeleteView.as_view(), name='delete comment'),
]
