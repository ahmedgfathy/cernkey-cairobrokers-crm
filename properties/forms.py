from django import forms
from .models import Property, PropertyType, PropertyStatus


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'address', 'city', 'state', 'zip_code', 'country',
                  'property_type', 'status', 'bedrooms', 'bathrooms', 'square_feet',
                  'lot_size', 'year_built', 'price', 'monthly_rent', 'hoa_fee',
                  'has_garage', 'garage_spaces', 'has_pool', 'has_garden', 'pet_friendly',
                  'main_image', 'is_featured', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'sap-input'}),
            'description': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 4}),
            'address': forms.TextInput(attrs={'class': 'sap-input'}),
            'city': forms.TextInput(attrs={'class': 'sap-input'}),
            'state': forms.TextInput(attrs={'class': 'sap-input'}),
            'zip_code': forms.TextInput(attrs={'class': 'sap-input'}),
            'country': forms.TextInput(attrs={'class': 'sap-input'}),
            'property_type': forms.Select(attrs={'class': 'sap-select'}),
            'status': forms.Select(attrs={'class': 'sap-select'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'sap-input'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'sap-input'}),
            'square_feet': forms.NumberInput(attrs={'class': 'sap-input'}),
            'lot_size': forms.NumberInput(attrs={'class': 'sap-input'}),
            'year_built': forms.NumberInput(attrs={'class': 'sap-input'}),
            'price': forms.NumberInput(attrs={'class': 'sap-input'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'sap-input'}),
            'hoa_fee': forms.NumberInput(attrs={'class': 'sap-input'}),
            'garage_spaces': forms.NumberInput(attrs={'class': 'sap-input'}),
            'main_image': forms.FileInput(attrs={'class': 'sap-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'sap-checkbox'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'sap-checkbox'}),
        }


class PropertyTypeForm(forms.ModelForm):
    class Meta:
        model = PropertyType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'sap-input'}),
            'description': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
        }


class PropertyStatusForm(forms.ModelForm):
    class Meta:
        model = PropertyStatus
        fields = ['name', 'color', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'sap-input'}),
            'color': forms.TextInput(attrs={'class': 'sap-input', 'type': 'color'}),
            'description': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
        }


class PropertySearchForm(forms.Form):
    query = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'sap-input', 'placeholder': 'Search properties...', 'onchange': 'this.form.submit()'
    }))
    min_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'sap-input', 'placeholder': 'Min Price', 'onchange': 'this.form.submit()'
    }))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'sap-input', 'placeholder': 'Max Price', 'onchange': 'this.form.submit()'
    }))
    bedrooms = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'class': 'sap-input', 'placeholder': 'Bedrooms', 'onchange': 'this.form.submit()'
    }))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'sap-input', 'placeholder': 'City', 'onchange': 'this.form.submit()'
    }))
