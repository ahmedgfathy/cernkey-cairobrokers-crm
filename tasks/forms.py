from django import forms
from .models import Task, TaskCategory, TaskPriority, TaskStatus


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'lead', 'related_property', 'opportunity',
                  'category', 'priority', 'status', 'assigned_to',
                  'due_date', 'due_time', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'sap-input'}),
            'description': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
            'lead': forms.Select(attrs={'class': 'sap-select'}),
            'related_property': forms.Select(attrs={'class': 'sap-select'}),
            'opportunity': forms.Select(attrs={'class': 'sap-select'}),
            'category': forms.Select(attrs={'class': 'sap-select'}),
            'priority': forms.Select(attrs={'class': 'sap-select'}),
            'status': forms.Select(attrs={'class': 'sap-select'}),
            'assigned_to': forms.Select(attrs={'class': 'sap-select'}),
            'due_date': forms.DateInput(attrs={'class': 'sap-input', 'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'class': 'sap-input', 'type': 'time'}),
            'start_date': forms.DateInput(attrs={'class': 'sap-input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'sap-input', 'type': 'date'}),
        }


class TaskCategoryForm(forms.ModelForm):
    class Meta:
        model = TaskCategory
        fields = ['name', 'color', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'sap-input'}),
            'color': forms.TextInput(attrs={'class': 'sap-input', 'type': 'color'}),
            'description': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
        }


class TaskPriorityForm(forms.ModelForm):
    class Meta:
        model = TaskPriority
        fields = ['name', 'color', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'sap-input'}),
            'color': forms.TextInput(attrs={'class': 'sap-input', 'type': 'color'}),
            'description': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
        }


class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = TaskStatus
        fields = ['name', 'color', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'sap-input'}),
            'color': forms.TextInput(attrs={'class': 'sap-input', 'type': 'color'}),
            'description': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
        }
