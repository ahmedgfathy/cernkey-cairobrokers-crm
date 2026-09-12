from django import forms
from .models import (Lead, LeadSource, LeadStatus, LeadTask, LeadCall,
                     LeadMeeting, LeadEmail, LeadNote)


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['first_name', 'last_name', 'email', 'phone', 'company',
                  'source', 'status', 'assigned_to', 'priority', 'notes']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'sap-input'}),
            'last_name': forms.TextInput(attrs={'class': 'sap-input'}),
            'email': forms.EmailInput(attrs={'class': 'sap-input'}),
            'phone': forms.TextInput(attrs={'class': 'sap-input'}),
            'company': forms.TextInput(attrs={'class': 'sap-input'}),
            'source': forms.Select(attrs={'class': 'sap-select'}),
            'status': forms.Select(attrs={'class': 'sap-select'}),
            'assigned_to': forms.Select(attrs={'class': 'sap-select'}),
            'priority': forms.Select(attrs={'class': 'sap-select'}),
            'notes': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
        }


class LeadSourceForm(forms.ModelForm):
    class Meta:
        model = LeadSource
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'sap-input'}),
            'description': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'sap-checkbox'}),
        }


class LeadStatusForm(forms.ModelForm):
    class Meta:
        model = LeadStatus
        fields = ['name', 'color', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'sap-input'}),
            'color': forms.TextInput(attrs={'class': 'sap-input', 'type': 'color'}),
            'description': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'sap-checkbox'}),
        }


class LeadTaskForm(forms.ModelForm):
    class Meta:
        model = LeadTask
        fields = ['title', 'description', 'task_type', 'status', 'priority',
                  'due_date', 'due_time', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'sap-input'}),
            'description': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
            'task_type': forms.Select(attrs={'class': 'sap-select'}),
            'status': forms.Select(attrs={'class': 'sap-select'}),
            'priority': forms.Select(attrs={'class': 'sap-select'}),
            'due_date': forms.DateInput(attrs={'class': 'sap-input', 'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'class': 'sap-input', 'type': 'time'}),
            'assigned_to': forms.Select(attrs={'class': 'sap-select'}),
        }


class LeadCallForm(forms.ModelForm):
    class Meta:
        model = LeadCall
        fields = ['call_date', 'duration_minutes', 'outcome', 'notes']
        widgets = {
            'call_date': forms.DateTimeInput(attrs={'class': 'sap-input', 'type': 'datetime-local'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'sap-input'}),
            'outcome': forms.Select(attrs={'class': 'sap-select'}),
            'notes': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
        }


class LeadMeetingForm(forms.ModelForm):
    class Meta:
        model = LeadMeeting
        fields = ['title', 'meeting_date', 'location', 'status', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'sap-input'}),
            'meeting_date': forms.DateTimeInput(attrs={'class': 'sap-input', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'sap-input'}),
            'status': forms.Select(attrs={'class': 'sap-select'}),
            'notes': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
        }


class LeadEmailForm(forms.ModelForm):
    class Meta:
        model = LeadEmail
        fields = ['subject', 'body', 'direction']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'sap-input'}),
            'body': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 5}),
            'direction': forms.Select(attrs={'class': 'sap-select'}),
        }


class LeadNoteForm(forms.ModelForm):
    class Meta:
        model = LeadNote
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3, 'placeholder': 'Add a note...'}),
        }
