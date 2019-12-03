from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from main.models import TaskComment, Task
from main.serializers import TaskCommentSerializer
from utils.permissions import IsOwnerOrReadOnly
import logging

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def task_comment_lists(request, pk):
    task = get_object_or_404(Task, id=pk)

    if request.method == 'GET':
        task_comments = TaskComment.objects.filter(task=task)
        serializer = TaskCommentSerializer(task_comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TaskCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user, task=task)
            logger.info('user with id: {} left comment'.format(request.user.id))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly))
def task_comment_detail(request, pk):
    task_comment = get_object_or_404(TaskComment, id=pk)

    if request.method == 'GET':
        serializer = TaskCommentSerializer(task_comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskCommentSerializer(instance=task_comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'DELETE':
        task_comment.delete()
        logger.info('user with id: {} deleted comment'.format(request.user.id))
        return Response(status=status.HTTP_204_NO_CONTENT)
