from django import forms
from .models import (Property, PropertyType, PropertyStatus, PropertyUnit,
                     PropertyViewing, PropertyOffer, PropertyNote)


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


class PropertyUnitForm(forms.ModelForm):
    class Meta:
        model = PropertyUnit
        fields = ['unit_number', 'floor', 'bedrooms', 'bathrooms', 'square_feet',
                  'monthly_rent', 'sale_price', 'status', 'description',
                  'tenant_name', 'tenant_phone', 'lease_start', 'lease_end']
        widgets = {
            'unit_number': forms.TextInput(attrs={'class': 'sap-input'}),
            'floor': forms.TextInput(attrs={'class': 'sap-input'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'sap-input'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'sap-input'}),
            'square_feet': forms.NumberInput(attrs={'class': 'sap-input'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'sap-input'}),
            'sale_price': forms.NumberInput(attrs={'class': 'sap-input'}),
            'status': forms.Select(attrs={'class': 'sap-select'}),
            'description': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
            'tenant_name': forms.TextInput(attrs={'class': 'sap-input'}),
            'tenant_phone': forms.TextInput(attrs={'class': 'sap-input'}),
            'lease_start': forms.DateInput(attrs={'class': 'sap-input', 'type': 'date'}),
            'lease_end': forms.DateInput(attrs={'class': 'sap-input', 'type': 'date'}),
        }


class PropertyViewingForm(forms.ModelForm):
    class Meta:
        model = PropertyViewing
        fields = ['prospect_name', 'prospect_phone', 'prospect_email',
                  'viewing_date', 'status', 'notes', 'feedback']
        widgets = {
            'prospect_name': forms.TextInput(attrs={'class': 'sap-input'}),
            'prospect_phone': forms.TextInput(attrs={'class': 'sap-input'}),
            'prospect_email': forms.EmailInput(attrs={'class': 'sap-input'}),
            'viewing_date': forms.DateTimeInput(attrs={'class': 'sap-input', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'sap-select'}),
            'notes': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
            'feedback': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
        }


class PropertyOfferForm(forms.ModelForm):
    class Meta:
        model = PropertyOffer
        fields = ['buyer_name', 'buyer_phone', 'buyer_email', 'offer_amount',
                  'offer_date', 'closing_date', 'status', 'notes']
        widgets = {
            'buyer_name': forms.TextInput(attrs={'class': 'sap-input'}),
            'buyer_phone': forms.TextInput(attrs={'class': 'sap-input'}),
            'buyer_email': forms.EmailInput(attrs={'class': 'sap-input'}),
            'offer_amount': forms.NumberInput(attrs={'class': 'sap-input'}),
            'offer_date': forms.DateInput(attrs={'class': 'sap-input', 'type': 'date'}),
            'closing_date': forms.DateInput(attrs={'class': 'sap-input', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'sap-select'}),
            'notes': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3}),
        }


class PropertyNoteForm(forms.ModelForm):
    class Meta:
        model = PropertyNote
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 3, 'placeholder': 'Add a note...'}),
        }
