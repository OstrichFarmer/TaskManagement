# from django.shortcuts import render
# from rest_framework import viewsets, permissions
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import filters
# from .models import Task
# from .serializers import TaskSerializer

# class TaskViewSet(viewsets.ModelViewSet):
#     """
#     A viewset that provides the standard actions
#     for creating, reading, updating, and deleting tasks.
#     """
#     serializer_class = TaskSerializer
#     permission_classes = [permissions.IsAuthenticated]  # Require authentication for all task actions
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # Add filter backends
#     filterset_fields = ['status', 'priority', 'due_date']  # Fields to filter by
#     ordering_fields = ['due_date', 'priority']  # Fields to order by

#     def get_queryset(self):
#         # Only return tasks that belong to the currently authenticated user
#         return Task.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         # Automatically associate the logged-in user with the created task
#         serializer.save(user=self.request.user)

from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Task
from .serializers import TaskSerializer

def base_view(request):
    return render(request, 'base.html')

# Task API ViewSet
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'due_date']
    ordering_fields = ['due_date', 'priority']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Dashboard view
@login_required
def dashboard_view(request):
    # Filter tasks by the authenticated user
    tasks = Task.objects.filter(user=request.user)

    # Get query parameters for filtering
    status = request.GET.get('status')
    priority = request.GET.get('priority')

    # Filter tasks based on status and priority if provided
    if status:
        tasks = tasks.filter(status=status)
    if priority:
        tasks = tasks.filter(priority=priority)

    return render(request, 'dashboard.html', {'tasks': tasks})

# Create Task view
@login_required
def create_task_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')

        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority
        )
        return redirect('dashboard')

    return render(request, 'create_task.html')


def complete_task_view(request, task_id):
    if request.method == 'POST':  # Ensure this view only responds to POST requests
        task = get_object_or_404(Task, id=task_id)
        task.status = 'completed'  # Adjust this based on your status field
        task.save()
        return redirect('dashboard') 

# Update Task view
@login_required
def update_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.due_date = request.POST.get('due_date')
        task.priority = request.POST.get('priority')
        task.save()
        return redirect('dashboard')

    return render(request, 'update_task.html', {'task': task})

# Task Detail view
@login_required
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

# Delete Task view
@login_required
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')
    return render(request, 'tasks/delete_task.html', {'task': task})


# Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login') 
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')  # Ensure 'login' is defined in URLs

# AJAX Task Creation View
@login_required
def task_create_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        if title and due_date:
            task = Task.objects.create(
                user=request.user,
                title=title,
                description=description,
                due_date=due_date,
                priority=priority
            )
            return JsonResponse({'status': 'success', 'task': task.title})
    return JsonResponse({'status': 'failed'}, status=400)
