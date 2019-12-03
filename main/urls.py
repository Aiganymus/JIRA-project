from django.urls import path
from rest_framework import routers

from main.views import ProjectListAPIView, \
    ProjectDetailAPIView, BlockListView, BlockDetailView, TaskViewSet, \
    MemberProjectViewSet, TaskDocumentViewSet, \
    task_comment_lists, task_comment_detail

urlpatterns = [
    path('projects/', ProjectListAPIView.as_view()),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view()),
    path('blocks/', BlockListView.as_view()),
    path('blocks/<int:pk>/', BlockDetailView.as_view()),
    path('tasks/<int:pk>/comments/', task_comment_lists),
    path('comments/<int:pk>/', task_comment_detail)
]

router = routers.DefaultRouter()
router.register('tasks', TaskViewSet, base_name='api')
router.register('project_members', MemberProjectViewSet, base_name='api')
router.register('task_documents', TaskDocumentViewSet, base_name='api')

urlpatterns += router.urls
