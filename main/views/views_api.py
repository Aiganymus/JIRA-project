from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from main.models import Project
from main.serializers import ProjectShortSerializer, ProjectDetailSerializer, ProjectFullSerializer
from rest_framework import status as status_codes
from django.shortcuts import get_object_or_404

from utils.permissions import IsOwnerOrReadOnly


class ProjectListAPIView(APIView):
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectShortSerializer(projects, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = ProjectFullSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(data=serializer.data, status=status_codes.HTTP_201_CREATED)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)


class ProjectDetailAPIView(APIView):
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectFullSerializer(instance=project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return Response(status=status_codes.HTTP_204_NO_CONTENT)
