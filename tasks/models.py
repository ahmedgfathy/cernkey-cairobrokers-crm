from django.db import models
from django.contrib.auth import get_user_model
from leads.models import Lead
from properties.models import Property
from opportunities.models import Opportunity
from datetime import date

User = get_user_model()


class TaskCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#6f42c1')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tasks_task_category'


class TaskPriority(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#fd7e14')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tasks_task_priority'


class TaskStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#20c997')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tasks_task_status'


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    related_property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True, related_name='task_items')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')

    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.ForeignKey(TaskPriority, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(TaskStatus, on_delete=models.SET_NULL, null=True, blank=True)

    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tasks')

    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        if self.due_date and not self.is_completed:
            return self.due_date < date.today()
        return False

    class Meta:
        db_table = 'tasks_task'
        ordering = ['-created_at']
