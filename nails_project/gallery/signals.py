from django.dispatch import receiver
from django.db.models.signals import pre_delete
from cloudinary import uploader
from nails_project.gallery.models import Gallery


@receiver(pre_delete, sender=Gallery)
def delete_media_when_account_deleted(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = Gallery.objects.get(pk=instance.pk).image
        except Gallery.DoesNotExist:
            return
        else:
            if old_image.public_id:
                uploader.destroy(old_image.public_id)
