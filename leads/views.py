from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime, parse_time
from urllib.parse import urlencode
from .models import (Lead, LeadSource, LeadStatus, LeadTask, LeadCall,
                     LeadMeeting, LeadEmail, LeadNote, LeadSavedFilter)
from .forms import (LeadForm, LeadSourceForm, LeadStatusForm, LeadTaskForm,
                    LeadCallForm, LeadMeetingForm, LeadEmailForm, LeadNoteForm)
from core.import_export import (export_csv, export_excel, parse_uploaded_file,
                                auto_match_headers, store_import_data,
                                load_import_data, clear_import_data)


LEAD_LIST_COLUMNS = {
    'name': 'Name',
    'email': 'Email',
    'phone': 'Phone',
    'company': 'Company',
    'source': 'Source',
    'status': 'Status',
    'assigned_to': 'Assigned To',
    'priority': 'Priority',
    'created_at': 'Created',
    'actions': 'Actions',
}
DEFAULT_LEAD_COLUMNS = list(LEAD_LIST_COLUMNS)
LEAD_FILTER_KEYS = ('q', 'status', 'priority', 'source', 'per_page')


def _valid_lead_columns(columns):
    selected = [column for column in columns if column in LEAD_LIST_COLUMNS]
    return selected or DEFAULT_LEAD_COLUMNS.copy()


@login_required
def lead_list(request):
    leads = Lead.objects.all()
    saved_filters = LeadSavedFilter.objects.filter(user=request.user)
    saved_view_id = request.GET.get('view')
    saved_view = saved_filters.filter(pk=saved_view_id).first() if saved_view_id else None
    has_new_filter = any(request.GET.get(key) for key in LEAD_FILTER_KEYS) or request.GET.getlist('columns')
    last_view = saved_filters.filter(is_last_used=True).first()
    view_filters = saved_view or (last_view if not has_new_filter else None)
    saved_values = view_filters.filters if view_filters else {}
    query = request.GET.get('q', saved_values.get('q', ''))
    status_id = request.GET.get('status', saved_values.get('status', ''))
    priority = request.GET.get('priority', saved_values.get('priority', ''))
    source_id = request.GET.get('source', saved_values.get('source', ''))
    per_page = request.GET.get('per_page', saved_values.get('per_page', '25'))
    selected_columns = _valid_lead_columns(
        request.GET.getlist('columns') or (view_filters.columns if view_filters else DEFAULT_LEAD_COLUMNS)
    )

    if saved_view:
        saved_filters.update(is_last_used=False)
        saved_view.is_last_used = True
        saved_view.save(update_fields=['is_last_used', 'updated_at'])

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

    leads = leads.select_related('source', 'status', 'assigned_to').order_by('-created_at')

    try:
        per_page = int(per_page)
        if per_page not in [10, 25, 50, 100]:
            per_page = 25
    except (ValueError, TypeError):
        per_page = 25

    paginator = Paginator(leads, per_page)
    page_number = request.GET.get('page', '1')
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'leads': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'query': query,
        'statuses': LeadStatus.objects.filter(is_active=True),
        'sources': LeadSource.objects.filter(is_active=True),
        'selected_status': status_id,
        'selected_priority': priority,
        'selected_source': source_id,
        'per_page': per_page,
        'page_sizes': [10, 25, 50, 100],
        'columns': LEAD_LIST_COLUMNS,
        'selected_columns': selected_columns,
        'saved_filters': saved_filters,
        'active_saved_filter': view_filters,
        'column_query': urlencode([('columns', column) for column in selected_columns]),
        'prev_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
    }
    return render(request, 'leads/lead_list.html', context)


@login_required
def lead_save_filter(request):
    if request.method != 'POST':
        return redirect('lead_list')
    name = request.POST.get('name', '').strip()
    if not name:
        messages.error(request, 'Enter a name for this saved filter.')
        return redirect('lead_list')
    columns = _valid_lead_columns(request.POST.getlist('columns'))
    filters = {key: request.POST.get(key, '').strip() for key in LEAD_FILTER_KEYS}
    saved_filter, _ = LeadSavedFilter.objects.update_or_create(
        user=request.user,
        name=name,
        defaults={'columns': columns, 'filters': filters, 'is_last_used': True},
    )
    LeadSavedFilter.objects.filter(user=request.user).exclude(pk=saved_filter.pk).update(is_last_used=False)
    messages.success(request, f'Saved filter "{name}" is ready to use.')
    return HttpResponseRedirect(f'/leads/?view={saved_filter.pk}')


@login_required
def lead_delete_filter(request, pk):
    if request.method == 'POST':
        LeadSavedFilter.objects.filter(user=request.user, pk=pk).delete()
        messages.success(request, 'Saved filter deleted.')
    return redirect('lead_list')


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


LEAD_EXPORT_FIELDS = [
    'first_name', 'last_name', 'email', 'phone', 'company',
    'source__name', 'status__name', 'assigned_to__first_name',
    'priority', 'notes', 'created_at',
]
LEAD_EXPORT_HEADERS = [
    'First Name', 'Last Name', 'Email', 'Phone', 'Company',
    'Source', 'Status', 'Assigned To',
    'Priority', 'Notes', 'Created At',
]
LEAD_DB_FIELDS = {
    'first_name': 'First Name',
    'last_name': 'Last Name',
    'email': 'Email',
    'phone': 'Phone',
    'company': 'Company',
    'source': 'Source',
    'status': 'Status',
    'assigned_to': 'Assigned To',
    'priority': 'Priority',
    'notes': 'Notes',
    'task_title': 'Task Title',
    'task_description': 'Task Description',
    'task_type': 'Task Type',
    'task_status': 'Task Status',
    'task_priority': 'Task Priority',
    'task_due_date': 'Task Due Date',
    'task_due_time': 'Task Due Time',
    'call_date': 'Call Date',
    'call_duration_minutes': 'Call Duration (minutes)',
    'call_outcome': 'Call Outcome',
    'call_notes': 'Call Notes',
    'meeting_title': 'Meeting Title',
    'meeting_date': 'Meeting Date',
    'meeting_location': 'Meeting Location',
    'meeting_status': 'Meeting Status',
    'meeting_notes': 'Meeting Notes',
    'email_subject': 'Email Subject',
    'email_body': 'Email Body',
    'email_direction': 'Email Direction',
    'email_sent_at': 'Email Sent At',
    'note_content': 'Note Content',
    # Legacy Leads.csv fields
    'lead_number': 'Lead Number',
    'salutation': 'Salutation',
    'call_result': 'المكالمه',
    'last_follow_up': 'اخر متابعه',
    'customer_status': 'حاله العميل',
    'assigned_to_name': 'Assigned To (legacy name)',
    'interested_unit_type': 'نوع الوحده المهتم بها العميل',
    'legacy_created_time': 'Created Time',
    'activity_type': 'نوع النشاط',
    'legacy_modified_time': 'Modified Time',
    'feedback': 'فيدباك',
    'legacy_description': 'Description',
    'last_modified_by_name': 'Last Modified By',
}

LEAD_LEGACY_FIELDS = (
    'lead_number', 'salutation', 'call_result', 'last_follow_up',
    'customer_status', 'assigned_to_name', 'interested_unit_type',
    'legacy_created_time', 'activity_type', 'legacy_modified_time', 'feedback',
    'legacy_description', 'last_modified_by_name',
)


def _import_datetime(value, date_only=False, time_only=False):
    if not value:
        return None
    value = str(value).strip()
    if date_only:
        return parse_date(value)
    if time_only:
        return parse_time(value)
    parsed = parse_datetime(value) or parse_datetime(value.replace(' ', 'T'))
    if parsed and timezone.is_naive(parsed):
        return timezone.make_aware(parsed)
    return parsed


def _create_import_activities(lead, data, user):
    if data.get('task_title'):
        due_date = _import_datetime(data.get('task_due_date'), date_only=True)
        due_time = _import_datetime(data.get('task_due_time'), time_only=True)
        task_type = data.get('task_type', '').lower()
        task_status = data.get('task_status', '').lower()
        task_priority = data.get('task_priority', '').lower()
        LeadTask.objects.create(
            lead=lead,
            title=data['task_title'][:200],
            description=data.get('task_description', ''),
            task_type=task_type if task_type in dict(LeadTask.TASK_TYPE_CHOICES) else 'other',
            status=task_status if task_status in dict(LeadTask.STATUS_CHOICES) else 'pending',
            priority=task_priority if task_priority in dict(LeadTask.PRIORITY_CHOICES) else 'medium',
            due_date=due_date,
            due_time=due_time,
            assigned_to=lead.assigned_to,
        )

    if any(data.get(field) for field in ('call_date', 'call_duration_minutes', 'call_outcome', 'call_notes')):
        try:
            duration = int(data.get('call_duration_minutes') or 0)
        except (TypeError, ValueError):
            duration = 0
        outcome = data.get('call_outcome', '').lower()
        LeadCall.objects.create(
            lead=lead,
            call_date=_import_datetime(data.get('call_date')) or timezone.now(),
            duration_minutes=max(duration, 0),
            outcome=outcome if outcome in dict(LeadCall.OUTCOME_CHOICES) else 'connected',
            notes=data.get('call_notes', ''),
            called_by=user,
        )

    if data.get('meeting_title'):
        meeting_status = data.get('meeting_status', '').lower()
        LeadMeeting.objects.create(
            lead=lead,
            title=data['meeting_title'][:200],
            meeting_date=_import_datetime(data.get('meeting_date')) or timezone.now(),
            location=data.get('meeting_location', '')[:300],
            status=meeting_status if meeting_status in dict(LeadMeeting.STATUS_CHOICES) else 'scheduled',
            notes=data.get('meeting_notes', ''),
            organized_by=user,
        )

    if data.get('email_subject'):
        direction = data.get('email_direction', '').lower()
        LeadEmail.objects.create(
            lead=lead,
            subject=data['email_subject'][:300],
            body=data.get('email_body', ''),
            direction=direction if direction in dict(LeadEmail.DIRECTION_CHOICES) else 'outgoing',
            sent_at=_import_datetime(data.get('email_sent_at')) or timezone.now(),
            sent_by=user,
        )

    if data.get('note_content'):
        LeadNote.objects.create(lead=lead, content=data['note_content'], created_by=user)


@login_required
def lead_export_csv(request):
    leads = Lead.objects.select_related('source', 'status', 'assigned_to').all()
    return export_csv(leads, LEAD_EXPORT_FIELDS, LEAD_EXPORT_HEADERS, 'leads_export')


@login_required
def lead_export_excel(request):
    leads = Lead.objects.select_related('source', 'status', 'assigned_to').all()
    return export_excel(leads, LEAD_EXPORT_FIELDS, LEAD_EXPORT_HEADERS, 'leads_export')


@login_required
def lead_import(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            try:
                headers, rows = parse_uploaded_file(file)
            except (OSError, ValueError, ImportError) as exc:
                messages.error(request, f'Could not read this file: {exc}')
                return redirect('lead_import')
            if not headers:
                messages.error(request, 'Could not parse the uploaded file. Add a header row and at least one data row.')
                return redirect('lead_import')
            auto_map = auto_match_headers(headers, LEAD_DB_FIELDS)
            # The legacy export calls the main phone field "MOBILE 1".
            for index, header in enumerate(headers):
                if header.strip().casefold() == 'mobile 1':
                    auto_map[index] = 'phone'
            store_import_data(request, 'leads', headers, rows)
            request.session['lead_import_auto_map'] = {str(k): v for k, v in auto_map.items()}
            return redirect('lead_import_map')
        elif 'confirm' in request.POST:
            mapping = {}
            for idx_str, field in request.POST.items():
                if idx_str.startswith('col_') and field:
                    try:
                        idx = int(idx_str.replace('col_', ''))
                    except ValueError:
                        continue
                    if field in LEAD_DB_FIELDS:
                        mapping[idx] = field
            headers, rows = load_import_data(request, 'leads')
            if not headers or not rows:
                messages.error(request, 'This import session has expired. Upload the file again.')
                return redirect('lead_import')
            created = 0
            updated = 0
            skipped = 0
            errors = []
            for row_idx, row in enumerate(rows):
                data = {}
                for idx_str, field in mapping.items():
                    if field not in LEAD_DB_FIELDS:
                        continue
                    idx = int(idx_str)
                    if idx < len(row):
                        data[field] = str(row[idx]).strip()
                if not any(data.values()):
                    skipped += 1
                    continue
                lead_data = {
                    'first_name': data.get('first_name', ''),
                    'last_name': data.get('last_name', ''),
                    'email': data.get('email', ''),
                    'phone': data.get('phone', ''),
                    'company': data.get('company', ''),
                    'priority': data.get('priority', 'medium').lower(),
                    'notes': data.get('notes', ''),
                }
                for field in LEAD_LEGACY_FIELDS:
                    lead_data[field] = data.get(field, '')
                if not lead_data['notes']:
                    lead_data['notes'] = lead_data['legacy_description']
                if lead_data['priority'] not in ['low', 'medium', 'high']:
                    lead_data['priority'] = 'medium'
                if data.get('source'):
                    source, _ = LeadSource.objects.get_or_create(name=data['source'])
                    lead_data['source'] = source
                if data.get('status'):
                    status, _ = LeadStatus.objects.get_or_create(name=data['status'])
                    lead_data['status'] = status
                assigned_name = data.get('assigned_to_name') or data.get('assigned_to')
                if assigned_name:
                    lead_data['assigned_to_name'] = assigned_name
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    agent = User.objects.filter(
                        Q(first_name__icontains=assigned_name.strip()) |
                        Q(last_name__icontains=assigned_name.strip()) |
                        Q(username__iexact=assigned_name.strip())
                    ).first()
                    if agent:
                        lead_data['assigned_to'] = agent
                try:
                    if lead_data['customer_status'] and not lead_data.get('status'):
                        status, _ = LeadStatus.objects.get_or_create(name=lead_data['customer_status'])
                        lead_data['status'] = status
                    if lead_data['lead_number']:
                        existing = Lead.objects.filter(lead_number__iexact=lead_data['lead_number']).first()
                    elif lead_data['email']:
                        existing = Lead.objects.filter(email=lead_data['email']).first()
                    else:
                        existing = None
                    if existing:
                        for k, v in lead_data.items():
                            setattr(existing, k, v)
                        existing.save()
                        lead = existing
                        updated += 1
                    else:
                        lead_data['created_by'] = request.user
                        lead = Lead.objects.create(**lead_data)
                        created += 1
                    _create_import_activities(lead, data, request.user)
                except Exception as e:
                    errors.append(f"Row {row_idx + 2}: {str(e)}")
            clear_import_data(request, 'leads')
            request.session.pop('lead_import_auto_map', None)
            msg = f'Import complete: {created} created, {updated} updated, {skipped} skipped.'
            if errors:
                msg += f' {len(errors)} row errors. ' + ' '.join(errors[:3])
                messages.warning(request, msg)
            else:
                messages.success(request, msg)
            return redirect('lead_list')
    return render(request, 'leads/lead_import.html', {
        'db_fields': LEAD_DB_FIELDS,
    })


@login_required
def lead_import_map(request):
    headers, rows = load_import_data(request, 'leads')
    auto_map = request.session.get('lead_import_auto_map', {})
    if not headers:
        messages.error(request, 'No import data found. Please upload a file first.')
        return redirect('lead_import')
    preview_rows = rows[:5]
    columns = []
    for index, header in enumerate(headers):
        sample = next((row[index] for row in preview_rows if index < len(row) and row[index]), '')
        columns.append({
            'index': index,
            'header': header or f'Column {index + 1}',
            'sample': sample,
            'mapped_field': auto_map.get(str(index), auto_map.get(index, '')),
        })
    mapped_fields = {column['mapped_field'] for column in columns}
    return render(request, 'leads/lead_import_map.html', {
        'headers': headers,
        'preview_rows': preview_rows,
        'total_rows': len(rows),
        'auto_map': auto_map,
        'columns': columns,
            'mapped_count': len(mapped_fields - {''}),
            'unmapped_count': len(headers) - len(auto_map),
            'missing_required': [],
            'db_fields': LEAD_DB_FIELDS,
        })


@login_required
def lead_cleanup(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'remove_duplicates':
            from django.db.models import Count
            duplicates = (
                Lead.objects.values('first_name', 'last_name', 'email', 'phone', 'company')
                .annotate(cnt=Count('id'))
                .filter(cnt__gt=1)
            )
            removed = 0
            for dup in duplicates:
                leads = Lead.objects.filter(
                    first_name=dup['first_name'],
                    last_name=dup['last_name'],
                    email=dup['email'],
                    phone=dup['phone'],
                    company=dup['company'],
                )
                keep = leads.first()
                to_delete = leads.exclude(pk=keep.pk)
                count = to_delete.count()
                to_delete.delete()
                removed += count
            messages.success(request, f'Removed {removed} duplicate leads.')
            return redirect('lead_list')
        elif action == 'remove_all':
            count = Lead.objects.count()
            Lead.objects.all().delete()
            messages.success(request, f'Removed all {count} leads.')
            return redirect('lead_list')
    duplicates_count = 0
    from django.db.models import Count
    dups = (
        Lead.objects.values('first_name', 'last_name', 'email', 'phone', 'company')
        .annotate(cnt=Count('id'))
        .filter(cnt__gt=1)
    )
    for dup in dups:
        duplicates_count += dup['cnt'] - 1
    return render(request, 'leads/lead_cleanup.html', {
        'total_leads': Lead.objects.count(),
        'duplicates_count': duplicates_count,
    })
