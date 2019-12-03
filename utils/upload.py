import os
import shutil
from django.conf import settings


def task_document_path(instance, filename):
    task_id = instance.task.id
    project_id = instance.task.block.project.id
    return 'projects/{}/{}/{}'.format(project_id, task_id, filename)


def task_delete_path(instance):
    path = os.path.abspath(os.path.join(settings.MEDIA_ROOT,
                                        'projects/{}/{}'.format(instance.block.project_id, instance.id)))
    shutil.rmtree(path)


def avatar_path(instance, filename):
    user_id = instance.user.id
    return 'avatars/{}/{}'.format(user_id, filename)


def avatar_delete_path(profile):
    path = os.path.abspath(os.path.join(settings.MEDIA_ROOT,
                                        'avatars/{}'.format(profile.user.id)))
    shutil.rmtree(path)