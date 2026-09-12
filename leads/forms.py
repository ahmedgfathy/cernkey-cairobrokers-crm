from django import forms
from .models import Lead, LeadSource, LeadStatus


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
