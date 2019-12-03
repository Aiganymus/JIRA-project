from rest_framework import generics
from rest_framework import mixins
from main.models import Block, Project
from main.serializers import BlockShortSerializer, BlockFullSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status as status_codes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class BlockListView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = Block.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BlockShortSerializer
        else:
            return BlockFullSerializer

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.request.data['project_id'])
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BlockDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockFullSerializer
    permission_classes = (IsAuthenticated, )
