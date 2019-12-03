from datetime import datetime

from django.db import models
from django.db.models import Q, Count

from utils import upload, validators
from users.models import MainUser
from utils.constants import BLOCK_NEW, BLOCK_TYPES
from utils.validators import block_type


class ProjectManager(models.Manager):
    def search_by_name(self, name):
        return self.filter(name__contains=name)

    def filter_by_creator(self, creator):
        return self.filter(creator=creator)

    def popular_projects(self, limit=10, offset=0):
        return self.all().annotate(members=Count('members')).order_by('members')[offset:limit]

    def today_projects(self):
        today = datetime.now()
        return self.filter(created_at__day=today.day,
                           created_at__month=today.month,
                           created_at__year=today.year)


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='created_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    projects = ProjectManager()

    class Meta:
        db_table = 'project'
        ordering = ('created_at', )

    def __str__(self):
        return self.name + '\n' + self.description

    def get_short_description(self):
        return self.description[: 10] + '...'


class ProjectMember(models.Model):
    member = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='assigned_projects')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    joined_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'project_member'
        ordering = ('joined_at', )

    def __str__(self):
        return self.project.name + ' member ' + self.member.full_name


class BlockManager(models.Manager):
    def filter_by_type(self, type):
        return self.filter(type=type)

    def filter_by_project(self, project):
        return self.filter(project=project)

    def order_by(self, value):
        return self.order_by(value)

    def get_tasks_count(self):
        return self.annotate(tasks=Count('tasks'))


class Block(models.Model):
    name = models.CharField(max_length=20)
    type = models.PositiveSmallIntegerField(choices=BLOCK_TYPES, default=BLOCK_NEW, validators=[block_type])
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='blocks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    blocks = BlockManager()

    class Meta:
        db_table = 'block'
        ordering = ('type', )

    def __str__(self):
        return self.name + ' ' + self.project.name


class TaskManager(models.Manager):
    def tasks_by_block(self, block):
        return self.filter(block=block)

    def tasks_by_creator_and_block(self, block, user):
        return self.filter(Q(block=block) & Q(creator=user))

    def tasks_by_executor_and_block(self, block, user):
        return self.filter(Q(block=block) & Q(executor=user))

    def order_by(self, value):
        return self.order_by(value)


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField()
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='tasks')
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='creator_tasks')
    executor = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='executor_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    tasks = TaskManager()

    class Meta:
        db_table = 'task'
        ordering = ('block', 'order', )

    def __str__(self):
        return self.name + '\n' + self.description


class TaskDocument(models.Model):
    document = models.FileField(upload_to=upload.task_document_path,
                                validators=[validators.task_document_size, validators.task_document_extension],
                                null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='documents')
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='uploaded_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'task_document'
        ordering = ('created_at', )

    @staticmethod
    def get_doc_len(doc):
        return len(doc.document)


class TaskCommentManager(models.Manager):
    def filter_by_creator(self, creator):
        return self.filter(creator=creator)

    def filter_by_task(self, task):
        return self.filter(task=task)

    def get_long_comments(self):
        return self.filter(body_len__gte=500)

    def order_by(self, value):
        return self.order_by(value)


class TaskComment(models.Model):
    body = models.TextField(max_length=500)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='creator_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'task_comment'
        ordering = ('created_at', )

    def __str__(self):
        return self.creator.username + ': ' + self.body
