from django.urls import path
from nails_project.accounts import views

urlpatterns = (
    path('sign-in/', views.SignInView.as_view(), name='sign in user'),
    path('sign-out/', views.SignOutView.as_view(), name='sign out user'),
    path('sign-up/', views.SignUpView.as_view(), name='sign up user'),
    path('profile/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile details'),
    path('delete/<int:pk>/', views.ProfileDeleteView.as_view(), name='profile delete'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
)