from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField



# Create your models here.

UserModel = get_user_model()


class Nails(models.Model):
    POSITIVE = 'Positive'
    NEGATIVE = 'Negative'
    FEEDBACK_TYPE = (
        (POSITIVE, "Positive"),
        (NEGATIVE, "Negative")
    )
    PEDICURE = 'Pedicure'
    MANICURE = 'Manicure'
    NAILS_TYPE = (
        (PEDICURE, "Pedicure"),
        (MANICURE, 'Manicure'),
    )
    type = models.CharField(max_length=10, choices=NAILS_TYPE, default=MANICURE)
    feedback = models.CharField(max_length=10, choices=FEEDBACK_TYPE, default=POSITIVE)
    description = models.TextField(blank=False)
    image = CloudinaryField(
        resource_type='image',
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class Like(models.Model):
    nails = models.ForeignKey(Nails, on_delete=models.CASCADE)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


from .signals import *
