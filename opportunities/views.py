from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from .models import Opportunity, OpportunityStage
from .forms import OpportunityForm, OpportunityStageForm


@login_required
def opportunity_list(request):
    opportunities = Opportunity.objects.filter(is_active=True)
    stage_id = request.GET.get('stage', '')
    opp_type = request.GET.get('opportunity_type', '')

    if stage_id:
        opportunities = opportunities.filter(stage_id=stage_id)
    if opp_type:
        opportunities = opportunities.filter(opportunity_type=opp_type)

    stages = OpportunityStage.objects.filter(is_active=True)
    total_value = opportunities.aggregate(total=Sum('estimated_value'))['total'] or 0

    context = {
        'opportunities': opportunities,
        'stages': stages,
        'opportunity_types': Opportunity.OPPORTUNITY_TYPE_CHOICES,
        'selected_stage': stage_id,
        'selected_type': opp_type,
        'total_value': total_value,
    }
    return render(request, 'opportunities/opportunity_list.html', context)


@login_required
def opportunity_detail(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    return render(request, 'opportunities/opportunity_detail.html', {'opportunity': opportunity})


@login_required
def opportunity_create(request):
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opp = form.save(commit=False)
            opp.created_by = request.user
            opp.save()
            messages.success(request, 'Opportunity created successfully.')
            return redirect('opportunity_detail', pk=opp.pk)
    else:
        form = OpportunityForm()
    return render(request, 'opportunities/opportunity_form.html', {'form': form, 'action': 'Create'})


@login_required
def opportunity_update(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    if request.method == 'POST':
        form = OpportunityForm(request.POST, instance=opportunity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Opportunity updated successfully.')
            return redirect('opportunity_detail', pk=opportunity.pk)
    else:
        form = OpportunityForm(instance=opportunity)
    return render(request, 'opportunities/opportunity_form.html', {'form': form, 'action': 'Update', 'opportunity': opportunity})


@login_required
def opportunity_delete(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    if request.method == 'POST':
        opportunity.delete()
        messages.success(request, 'Opportunity deleted successfully.')
        return redirect('opportunity_list')
    return render(request, 'opportunities/opportunity_confirm_delete.html', {'opportunity': opportunity})


@login_required
def opportunity_stage_list(request):
    stages = OpportunityStage.objects.all()
    return render(request, 'opportunities/opportunity_stage_list.html', {'stages': stages})


@login_required
def opportunity_stage_create(request):
    if request.method == 'POST':
        form = OpportunityStageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Opportunity stage created successfully.')
            return redirect('opportunity_stage_list')
    else:
        form = OpportunityStageForm()
    return render(request, 'opportunities/opportunity_stage_form.html', {'form': form})


@login_required
def opportunity_stage_update(request, pk):
    stage = get_object_or_404(OpportunityStage, pk=pk)
    if request.method == 'POST':
        form = OpportunityStageForm(request.POST, instance=stage)
        if form.is_valid():
            form.save()
            messages.success(request, 'Opportunity stage updated successfully.')
            return redirect('opportunity_stage_list')
    else:
        form = OpportunityStageForm(instance=stage)
    return render(request, 'opportunities/opportunity_stage_form.html', {'form': form, 'stage': stage})


@login_required
def opportunity_stage_delete(request, pk):
    stage = get_object_or_404(OpportunityStage, pk=pk)
    if request.method == 'POST':
        stage.delete()
        messages.success(request, 'Opportunity stage deleted successfully.')
        return redirect('opportunity_stage_list')
    return render(request, 'opportunities/opportunity_stage_confirm_delete.html', {'stage': stage})
