from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status as status_codes

from main.models import Task, ProjectMember, TaskDocument
from main.serializers import TaskSerializerCreateUpdate, TaskSerializerGet, \
    MemberProjectSerializer, TaskDocumentSerializer

import logging

logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskSerializerGet
        else:
            return TaskSerializerCreateUpdate

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(creator=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)


class MemberProjectViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = MemberProjectSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class TaskDocumentViewSet(mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    queryset = TaskDocument.objects.all()
    serializer_class = TaskDocumentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(creator=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)
