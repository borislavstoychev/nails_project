from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from nails_project.accounts.manager import NailsUserManager
from cloudinary.models import CloudinaryField


class NailsUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    USERNAME_FIELD = 'email'

    objects = NailsUserManager()


class Profile(models.Model):
    first_name = models.CharField(
        max_length=20,
        blank=True,
    )
    last_name = models.CharField(
        max_length=20,
        blank=True,
    )
    phone_number = models.CharField(
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+359999999'. Up to 15 digits allowed.")],
        max_length=17,
        blank=True,
    )
    age = models.IntegerField(
        blank=True,
        null=True,
    )
    profile_image = CloudinaryField(
        resource_type='image',
        blank=True,
    )
    is_complete = models.BooleanField(
        default=False,
    )

    user = models.OneToOneField(
        NailsUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.user.email or ""


from .signals import *
