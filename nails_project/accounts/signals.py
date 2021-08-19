from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from cloudinary import uploader
from nails_project.accounts.models import Profile
from nails_project.nails.models import Feedback

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, **kwargs):
    if created:
        profile = Profile(
            user=instance,
        )
        profile.save()


@receiver(pre_save, sender=Profile)
def check_is_complete(sender, instance, **kwargs):
    if instance.first_name and instance.last_name and instance.phone_number:
        instance.is_complete = True
    else:
        instance.is_complete = False

    if instance.pk:
        try:
            old_avatar = Profile.objects.get(pk=instance.pk).profile_image
        except Profile.DoesNotExist:
            return
        else:
            try:
                new_avatar = instance.profile_image.url
            except AttributeError:
                if old_avatar.public_id is not None:
                    uploader.destroy(old_avatar.public_id)


@receiver(pre_delete, sender=UserModel)
def delete_media_when_account_deleted(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_avatar = Profile.objects.get(pk=instance.pk).profile_image
            old_user_media = Feedback.objects.filter(user_id=instance.pk)
        except Profile.DoesNotExist:
            return
        else:
            if old_avatar.public_id:
                uploader.destroy(old_avatar.public_id)
                for media in old_user_media:
                    uploader.destroy(media.image.public_id)
