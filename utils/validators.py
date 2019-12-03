import os
from django.core.exceptions import ValidationError
from utils.constants import TASK_ALLOWED_EXISTS, BLOCK_NEW, BLOCK_DONE, AVATAR_ALLOWED_EXISTS


def task_document_size(value):
    if value.size > 1000000:
        raise ValidationError('invalid file size')


def task_document_extension(value):
    ext = os.path.splitext(value.name)[1]

    if not ext.lower() in TASK_ALLOWED_EXISTS:
        raise ValidationError('not allowed ext, allowed ({})'.format(TASK_ALLOWED_EXISTS))


def avatar_extension(value):
    ext = os.path.splitext(value.name)[1]

    if not ext.lower() in AVATAR_ALLOWED_EXISTS:
        raise ValidationError('not allowed ext, allowed ({})'.format(AVATAR_ALLOWED_EXISTS))


def block_type(value):
    if BLOCK_NEW > value > BLOCK_DONE:
        raise ValidationError('block type must be: [0, 1, 2, 3]')