from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from cloudinary import uploader
from nails_project.nails.models import Feedback


@receiver(pre_save, sender=Feedback)
def remove_old_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = Feedback.objects.get(pk=instance.pk).image
        except Feedback.DoesNotExist:
            return
        else:
            try:
                new_image = instance.image.url
            except AttributeError:
                uploader.destroy(old_image.public_id)


@receiver(pre_delete, sender=Feedback)
def delete_media_when_account_deleted(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = Feedback.objects.get(pk=instance.pk).image
        except Feedback.DoesNotExist:
            return
        else:
            if old_image.public_id:
                uploader.destroy(old_image.public_id)