from django import forms
from .models import Document, DocumentType


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'document_type', 'file',
                  'related_lead_id', 'related_property_id', 'related_opportunity_id',
                  'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'sap-input'}),
            'description': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
            'document_type': forms.Select(attrs={'class': 'sap-select'}),
            'file': forms.FileInput(attrs={'class': 'sap-input'}),
            'related_lead_id': forms.NumberInput(attrs={'class': 'sap-input', 'placeholder': 'Lead ID'}),
            'related_property_id': forms.NumberInput(attrs={'class': 'sap-input', 'placeholder': 'Property ID'}),
            'related_opportunity_id': forms.NumberInput(attrs={'class': 'sap-input', 'placeholder': 'Opportunity ID'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'sap-checkbox'}),
        }


class DocumentTypeForm(forms.ModelForm):
    class Meta:
        model = DocumentType
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'sap-input'}),
            'description': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'sap-checkbox'}),
        }
