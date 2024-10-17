# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import TaskViewSet

# # Create a router and register our viewsets with it
# router = DefaultRouter()
# router.register(r'tasks', TaskViewSet, basename='task')

# # The API URLs are now determined automatically by the router.
# urlpatterns = [
#     path('', include(router.urls)),
# ]


# tasks/urls.py
from django.urls import path
from .views import (
    dashboard_view,
    create_task_view,
    update_task_view,
    task_detail_view,
    delete_task_view,
    register_view,
    login_view,
    logout_view,
    base_view,
    complete_task_view
)

urlpatterns = [
    path('', base_view, name='base'),  # Home page
    path('dashboard/', dashboard_view, name='dashboard'),
    path('create-task/', create_task_view, name='create_task'),
    path('update-task/<int:task_id>/', update_task_view, name='update_task'),
    path('task-detail/<int:task_id>/', task_detail_view, name='task_detail'),
    path('complete-task/<int:task_id>/', complete_task_view, name='task_complete'),
    path('delete-task/<int:task_id>/', delete_task_view, name='delete_task'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),  # Login page
    path('logout/', logout_view, name='logout'),  # Logout page
]

