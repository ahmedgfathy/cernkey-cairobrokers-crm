from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Notification


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user, is_archived=False)
    unread_count = notifications.filter(is_read=False).count()
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'notifications/notification_list.html', context)


@login_required
def notification_detail(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    if not notification.is_read:
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
    return render(request, 'notifications/notification_detail.html', {'notification': notification})


@login_required
def notification_mark_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    if request.method == 'POST':
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        messages.success(request, 'Notification marked as read.')
    return redirect('notification_list')


@login_required
def notification_mark_all_read(request):
    if request.method == 'POST':
        Notification.objects.filter(recipient=request.user, is_read=False).update(
            is_read=True, read_at=timezone.now()
        )
        messages.success(request, 'All notifications marked as read.')
    return redirect('notification_list')


@login_required
def notification_archive(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    if request.method == 'POST':
        notification.is_archived = True
        notification.save()
        messages.success(request, 'Notification archived.')
    return redirect('notification_list')


@login_required
def notification_delete(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    if request.method == 'POST':
        notification.delete()
        messages.success(request, 'Notification deleted.')
    return redirect('notification_list')
