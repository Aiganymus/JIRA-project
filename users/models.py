from django.db import models
from django.contrib.auth.models import AbstractUser
from jira import settings
from utils.upload import avatar_path
from utils.validators import avatar_extension


class MainUser(AbstractUser):
    class Meta:
        verbose_name = 'MainUser'
        verbose_name_plural = 'MainUsers'
        ordering = ('date_joined', )

    def __str__(self):
        return '{}: {}'.format(self.id, self.username)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Profile(models.Model):
    bio = models.TextField(max_length=500)
    avatar = models.FileField(upload_to=avatar_path, validators=[avatar_extension],  null=True)
    web_site = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField(max_length=300)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.user.username
