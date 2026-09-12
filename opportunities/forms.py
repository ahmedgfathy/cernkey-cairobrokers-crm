from django import forms
from .models import Opportunity, OpportunityStage


class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['name', 'description', 'opportunity_type', 'lead', 'related_property',
                  'stage', 'assigned_to', 'estimated_value', 'expected_close_date',
                  'probability', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'sap-input'}),
            'description': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
            'opportunity_type': forms.Select(attrs={'class': 'sap-select'}),
            'lead': forms.Select(attrs={'class': 'sap-select'}),
            'related_property': forms.Select(attrs={'class': 'sap-select'}),
            'stage': forms.Select(attrs={'class': 'sap-select'}),
            'assigned_to': forms.Select(attrs={'class': 'sap-select'}),
            'estimated_value': forms.NumberInput(attrs={'class': 'sap-input'}),
            'expected_close_date': forms.DateInput(attrs={'class': 'sap-input', 'type': 'date'}),
            'probability': forms.NumberInput(attrs={'class': 'sap-input', 'min': 0, 'max': 100}),
            'is_active': forms.CheckboxInput(attrs={'class': 'sap-checkbox'}),
        }


class OpportunityStageForm(forms.ModelForm):
    class Meta:
        model = OpportunityStage
        fields = ['name', 'color', 'description', 'probability', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'sap-input'}),
            'color': forms.TextInput(attrs={'class': 'sap-input', 'type': 'color'}),
            'description': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
            'probability': forms.NumberInput(attrs={'class': 'sap-input'}),
            'order': forms.NumberInput(attrs={'class': 'sap-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'sap-checkbox'}),
        }
