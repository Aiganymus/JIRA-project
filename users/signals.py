from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from users.models import MainUser, Profile
from utils.upload import avatar_delete_path


@receiver(post_save, sender=MainUser)
def user_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_delete, sender=Profile)
def profile_deleted(sender, instance, **kwargs):
    avatar_delete_path(instance)