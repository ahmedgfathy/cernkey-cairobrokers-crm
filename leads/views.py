from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Lead, LeadSource, LeadStatus
from .forms import LeadForm, LeadSourceForm, LeadStatusForm


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
    return render(request, 'leads/lead_detail.html', {'lead': lead})


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
