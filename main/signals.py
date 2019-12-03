from django.db.models.signals import post_delete
from django.dispatch import receiver

from main.models import Task
from utils.upload import task_delete_path


@receiver(post_delete, sender=Task)
def task_deleted(sender, instance, **kwargs):
    task_delete_path(instance)
