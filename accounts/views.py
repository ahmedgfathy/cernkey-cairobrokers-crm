from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, UserProfileForm, LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}! You can now log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard_view(request):
    from leads.models import Lead
    from properties.models import Property
    from opportunities.models import Opportunity
    from tasks.models import Task
    from notifications.models import Notification

    context = {
        'total_leads': Lead.objects.count(),
        'total_properties': Property.objects.filter(is_active=True).count(),
        'total_opportunities': Opportunity.objects.filter(is_active=True).count(),
        'total_tasks': Task.objects.filter(assigned_to=request.user, is_completed=False).count(),
        'unread_notifications': Notification.objects.filter(recipient=request.user, is_read=False).count(),
        'recent_leads': Lead.objects.order_by('-created_at')[:5],
        'recent_properties': Property.objects.filter(is_active=True).order_by('-created_at')[:5],
        'recent_opportunities': Opportunity.objects.filter(is_active=True).order_by('-created_at')[:5],
        'upcoming_tasks': Task.objects.filter(assigned_to=request.user, is_completed=False).order_by('due_date')[:5],
    }
    return render(request, 'accounts/dashboard.html', context)
