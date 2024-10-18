from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'

    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    PENDING = 'Pending'
    COMPLETED = 'Completed'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=MEDIUM)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    completed_at = models.DateTimeField(null=True, blank=True)  

    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title
