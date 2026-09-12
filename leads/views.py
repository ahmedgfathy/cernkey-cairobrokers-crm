from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import (Lead, LeadSource, LeadStatus, LeadTask, LeadCall,
                     LeadMeeting, LeadEmail, LeadNote)
from .forms import (LeadForm, LeadSourceForm, LeadStatusForm, LeadTaskForm,
                    LeadCallForm, LeadMeetingForm, LeadEmailForm, LeadNoteForm)


@login_required
def lead_list(request):
    leads = Lead.objects.all()
    query = request.GET.get('q', '')
    status_id = request.GET.get('status', '')
    priority = request.GET.get('priority', '')
    source_id = request.GET.get('source', '')

    if query:
        leads = leads.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) |
            Q(email__icontains=query) | Q(phone__icontains=query) |
            Q(company__icontains=query)
        )
    if status_id:
        leads = leads.filter(status_id=status_id)
    if priority:
        leads = leads.filter(priority=priority)
    if source_id:
        leads = leads.filter(source_id=source_id)

    context = {
        'leads': leads,
        'query': query,
        'statuses': LeadStatus.objects.filter(is_active=True),
        'sources': LeadSource.objects.filter(is_active=True),
        'selected_status': status_id,
        'selected_priority': priority,
        'selected_source': source_id,
    }
    return render(request, 'leads/lead_list.html', context)


@login_required
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    tasks = lead.lead_tasks.all()[:10]
    calls = lead.lead_calls.all()[:10]
    meetings = lead.lead_meetings.all()[:10]
    emails = lead.lead_emails.all()[:10]
    notes = lead.lead_notes.all()[:10]

    all_activities = []
    for t in tasks:
        all_activities.append({'type': 'task', 'title': t.title, 'date': t.created_at, 'status': t.status, 'icon': 'fa-tasks', 'color': '#6f42c1'})
    for c in calls:
        all_activities.append({'type': 'call', 'title': f"Call - {c.get_outcome_display()}", 'date': c.call_date, 'status': c.outcome, 'icon': 'fa-phone', 'color': '#007bff'})
    for m in meetings:
        all_activities.append({'type': 'meeting', 'title': m.title, 'date': m.meeting_date, 'status': m.get_status_display(), 'icon': 'fa-calendar', 'color': '#28a745'})
    for e in emails:
        all_activities.append({'type': 'email', 'title': e.subject, 'date': e.sent_at, 'status': e.get_direction_display(), 'icon': 'fa-envelope', 'color': '#fd7e14'})
    all_activities.sort(key=lambda x: x['date'], reverse=True)

    context = {
        'lead': lead,
        'tasks': tasks,
        'calls': calls,
        'meetings': meetings,
        'emails': emails,
        'notes': notes,
        'all_activities': all_activities[:20],
        'task_form': LeadTaskForm(),
        'call_form': LeadCallForm(),
        'meeting_form': LeadMeetingForm(),
        'email_form': LeadEmailForm(),
        'note_form': LeadNoteForm(),
    }
    return render(request, 'leads/lead_detail.html', context)


@login_required
def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.save()
            messages.success(request, 'Lead created successfully.')
            return redirect('lead_detail', pk=lead.pk)
    else:
        form = LeadForm()
    return render(request, 'leads/lead_form.html', {'form': form, 'action': 'Create'})


@login_required
def lead_update(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead updated successfully.')
            return redirect('lead_detail', pk=lead.pk)
    else:
        form = LeadForm(instance=lead)
    return render(request, 'leads/lead_form.html', {'form': form, 'action': 'Update', 'lead': lead})


@login_required
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        lead.delete()
        messages.success(request, 'Lead deleted successfully.')
        return redirect('lead_list')
    return render(request, 'leads/lead_confirm_delete.html', {'lead': lead})


@login_required
def lead_task_create(request, lead_pk):
    lead = get_object_or_404(Lead, pk=lead_pk)
    if request.method == 'POST':
        form = LeadTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.lead = lead
            task.assigned_to = request.user
            task.save()
            messages.success(request, 'Task created.')
    return redirect('lead_detail', pk=lead_pk)


@login_required
def lead_task_update(request, pk):
    task = get_object_or_404(LeadTask, pk=pk)
    if request.method == 'POST':
        form = LeadTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated.')
    return redirect('lead_detail', pk=task.lead.pk)


@login_required
def lead_task_complete(request, pk):
    task = get_object_or_404(LeadTask, pk=pk)
    from django.utils import timezone
    task.status = 'completed'
    task.completed_at = timezone.now()
    task.save()
    messages.success(request, 'Task marked as completed.')
    return redirect('lead_detail', pk=task.lead.pk)


@login_required
def lead_task_delete(request, pk):
    task = get_object_or_404(LeadTask, pk=pk)
    lead_pk = task.lead.pk
    task.delete()
    messages.success(request, 'Task deleted.')
    return redirect('lead_detail', pk=lead_pk)


@login_required
def lead_call_create(request, lead_pk):
    lead = get_object_or_404(Lead, pk=lead_pk)
    if request.method == 'POST':
        form = LeadCallForm(request.POST)
        if form.is_valid():
            call = form.save(commit=False)
            call.lead = lead
            call.called_by = request.user
            call.save()
            messages.success(request, 'Call logged.')
    return redirect('lead_detail', pk=lead_pk)


@login_required
def lead_call_delete(request, pk):
    call = get_object_or_404(LeadCall, pk=pk)
    lead_pk = call.lead.pk
    call.delete()
    messages.success(request, 'Call log deleted.')
    return redirect('lead_detail', pk=lead_pk)


@login_required
def lead_meeting_create(request, lead_pk):
    lead = get_object_or_404(Lead, pk=lead_pk)
    if request.method == 'POST':
        form = LeadMeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.lead = lead
            meeting.organized_by = request.user
            meeting.save()
            messages.success(request, 'Meeting scheduled.')
    return redirect('lead_detail', pk=lead_pk)


@login_required
def lead_meeting_delete(request, pk):
    meeting = get_object_or_404(LeadMeeting, pk=pk)
    lead_pk = meeting.lead.pk
    meeting.delete()
    messages.success(request, 'Meeting deleted.')
    return redirect('lead_detail', pk=lead_pk)


@login_required
def lead_email_create(request, lead_pk):
    lead = get_object_or_404(Lead, pk=lead_pk)
    if request.method == 'POST':
        form = LeadEmailForm(request.POST)
        if form.is_valid():
            email = form.save(commit=False)
            email.lead = lead
            email.sent_by = request.user
            email.save()
            messages.success(request, 'Email logged.')
    return redirect('lead_detail', pk=lead_pk)


@login_required
def lead_email_delete(request, pk):
    email = get_object_or_404(LeadEmail, pk=pk)
    lead_pk = email.lead.pk
    email.delete()
    messages.success(request, 'Email deleted.')
    return redirect('lead_detail', pk=lead_pk)


@login_required
def lead_note_create(request, lead_pk):
    lead = get_object_or_404(Lead, pk=lead_pk)
    if request.method == 'POST':
        form = LeadNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.lead = lead
            note.created_by = request.user
            note.save()
            messages.success(request, 'Note added.')
    return redirect('lead_detail', pk=lead_pk)


@login_required
def lead_note_delete(request, pk):
    note = get_object_or_404(LeadNote, pk=pk)
    lead_pk = note.lead.pk
    note.delete()
    messages.success(request, 'Note deleted.')
    return redirect('lead_detail', pk=lead_pk)


@login_required
def lead_source_list(request):
    sources = LeadSource.objects.all()
    return render(request, 'leads/lead_source_list.html', {'sources': sources})


@login_required
def lead_source_create(request):
    if request.method == 'POST':
        form = LeadSourceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead source created successfully.')
            return redirect('lead_source_list')
    else:
        form = LeadSourceForm()
    return render(request, 'leads/lead_source_form.html', {'form': form})


@login_required
def lead_source_update(request, pk):
    source = get_object_or_404(LeadSource, pk=pk)
    if request.method == 'POST':
        form = LeadSourceForm(request.POST, instance=source)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead source updated successfully.')
            return redirect('lead_source_list')
    else:
        form = LeadSourceForm(instance=source)
    return render(request, 'leads/lead_source_form.html', {'form': form, 'source': source})


@login_required
def lead_source_delete(request, pk):
    source = get_object_or_404(LeadSource, pk=pk)
    if request.method == 'POST':
        source.delete()
        messages.success(request, 'Lead source deleted successfully.')
        return redirect('lead_source_list')
    return render(request, 'leads/lead_source_confirm_delete.html', {'source': source})


@login_required
def lead_status_list(request):
    statuses = LeadStatus.objects.all()
    return render(request, 'leads/lead_status_list.html', {'statuses': statuses})


@login_required
def lead_status_create(request):
    if request.method == 'POST':
        form = LeadStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead status created successfully.')
            return redirect('lead_status_list')
    else:
        form = LeadStatusForm()
    return render(request, 'leads/lead_status_form.html', {'form': form})


@login_required
def lead_status_update(request, pk):
    status = get_object_or_404(LeadStatus, pk=pk)
    if request.method == 'POST':
        form = LeadStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead status updated successfully.')
            return redirect('lead_status_list')
    else:
        form = LeadStatusForm(instance=status)
    return render(request, 'leads/lead_status_form.html', {'form': form, 'status': status})


@login_required
def lead_status_delete(request, pk):
    status = get_object_or_404(LeadStatus, pk=pk)
    if request.method == 'POST':
        status.delete()
        messages.success(request, 'Lead status deleted successfully.')
        return redirect('lead_status_list')
    return render(request, 'leads/lead_status_confirm_delete.html', {'status': status})
