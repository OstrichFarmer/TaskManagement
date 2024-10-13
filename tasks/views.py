from django.shortcuts import render
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    for creating, reading, updating, and deleting tasks.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require authentication for all task actions
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # Add filter backends
    filterset_fields = ['status', 'priority', 'due_date']  # Fields to filter by
    ordering_fields = ['due_date', 'priority']  # Fields to order by

    def get_queryset(self):
        # Only return tasks that belong to the currently authenticated user
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the logged-in user with the created task
        serializer.save(user=self.request.user)
