from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Task, TaskCategory, TaskPriority, TaskStatus
from .forms import TaskForm, TaskCategoryForm, TaskPriorityForm, TaskStatusForm


@login_required
def task_list(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    status_id = request.GET.get('status', '')
    priority_id = request.GET.get('priority', '')
    category_id = request.GET.get('category', '')

    if status_id:
        tasks = tasks.filter(status_id=status_id)
    if priority_id:
        tasks = tasks.filter(priority_id=priority_id)
    if category_id:
        tasks = tasks.filter(category_id=category_id)

    context = {
        'tasks': tasks,
        'statuses': TaskStatus.objects.all(),
        'priorities': TaskPriority.objects.all(),
        'categories': TaskCategory.objects.all(),
        'selected_status': status_id,
        'selected_priority': priority_id,
        'selected_category': category_id,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Update', 'task': task})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.is_completed = True
        task.completed_at = timezone.now()
        task.save()
        messages.success(request, 'Task marked as completed.')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_complete.html', {'task': task})


@login_required
def task_category_list(request):
    categories = TaskCategory.objects.all()
    return render(request, 'tasks/task_category_list.html', {'categories': categories})


@login_required
def task_category_create(request):
    if request.method == 'POST':
        form = TaskCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task category created successfully.')
            return redirect('task_category_list')
    else:
        form = TaskCategoryForm()
    return render(request, 'tasks/task_category_form.html', {'form': form})


@login_required
def task_priority_list(request):
    priorities = TaskPriority.objects.all()
    return render(request, 'tasks/task_priority_list.html', {'priorities': priorities})


@login_required
def task_priority_create(request):
    if request.method == 'POST':
        form = TaskPriorityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task priority created successfully.')
            return redirect('task_priority_list')
    else:
        form = TaskPriorityForm()
    return render(request, 'tasks/task_priority_form.html', {'form': form})


@login_required
def task_status_list(request):
    statuses = TaskStatus.objects.all()
    return render(request, 'tasks/task_status_list.html', {'statuses': statuses})


@login_required
def task_status_create(request):
    if request.method == 'POST':
        form = TaskStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task status created successfully.')
            return redirect('task_status_list')
    else:
        form = TaskStatusForm()
    return render(request, 'tasks/task_status_form.html', {'form': form})
