from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'sap-input', 'placeholder': 'Enter your username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'sap-input', 'placeholder': 'Enter your password'
    }))


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'sap-input', 'placeholder': 'Email address'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'sap-input', 'placeholder': 'First name'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'sap-input', 'placeholder': 'Last name'
    }))
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, widget=forms.Select(attrs={
        'class': 'sap-select'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'sap-input', 'placeholder': 'Username'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'bio', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'sap-input'}),
            'last_name': forms.TextInput(attrs={'class': 'sap-input'}),
            'email': forms.EmailInput(attrs={'class': 'sap-input'}),
            'phone': forms.TextInput(attrs={'class': 'sap-input'}),
            'bio': forms.Textarea(attrs={'class': 'sap-textarea', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={'class': 'sap-input'}),
        }
