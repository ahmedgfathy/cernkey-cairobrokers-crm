from django.contrib import admin
from .models import Task, TaskCategory, TaskPriority, TaskStatus
from leads.models import Lead
from properties.models import Property
from opportunities.models import Opportunity

@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)

@admin.register(TaskPriority)
class TaskPriorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)

@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'category', 'priority', 'status', 'due_date', 'is_completed', 'created_at')
    list_filter = ('category', 'priority', 'status', 'assigned_to', 'is_completed', 'due_date', 'created_at')
    search_fields = ('title', 'description', 'assigned_to__username')
    readonly_fields = ('created_at', 'updated_at', 'completed_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description')
        }),
        ('Related Objects', {
            'fields': ('lead', 'related_property', 'opportunity'),
            'classes': ('collapse',)
        }),
        ('Task Details', {
            'fields': ('category', 'priority', 'status')
        }),
        ('Assignment & Scheduling', {
            'fields': ('assigned_to', 'created_by', 'due_date', 'due_time', 'start_date', 'end_date')
        }),
        ('Completion', {
            'fields': ('is_completed', 'completed_at')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
