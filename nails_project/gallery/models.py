from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
UserModel = get_user_model()


class Gallery(models.Model):
    image = CloudinaryField(
        resource_type='image',
        folder='gallery'
    )
    description = models.TextField(blank=False, max_length=200)


class LikeImage(models.Model):
    image = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class CommentImage(models.Model):
    image = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


from .signals import *


