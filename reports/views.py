from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q, Avg, F, Value
from django.db.models.functions import TruncMonth, TruncWeek
from django.utils import timezone
from datetime import timedelta
from leads.models import Lead, LeadSource, LeadStatus
from properties.models import Property, PropertyType, PropertyStatus
from opportunities.models import Opportunity, OpportunityStage
from tasks.models import Task, TaskCategory, TaskPriority, TaskStatus
from accounts.models import User


@login_required
def reports_dashboard(request):
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    seven_days_ago = now - timedelta(days=7)

    total_leads = Lead.objects.count()
    leads_this_month = Lead.objects.filter(created_at__gte=thirty_days_ago).count()
    leads_this_week = Lead.objects.filter(created_at__gte=seven_days_ago).count()

    total_properties = Property.objects.filter(is_active=True).count()
    properties_value = Property.objects.filter(is_active=True).aggregate(total=Sum('price'))['total'] or 0

    total_opps = Opportunity.objects.filter(is_active=True).count()
    total_value = Opportunity.objects.filter(is_active=True).aggregate(total=Sum('estimated_value'))['total'] or 0
    won_opps = Opportunity.objects.filter(is_active=True, actual_close_date__isnull=False).count()
    won_value = Opportunity.objects.filter(is_active=True, actual_close_date__isnull=False).aggregate(total=Sum('estimated_value'))['total'] or 0
    lost_opps = total_opps - won_opps
    win_rate = round((won_opps / total_opps * 100), 1) if total_opps > 0 else 0

    tasks_total = Task.objects.count()
    tasks_completed = Task.objects.filter(is_completed=True).count()
    tasks_overdue = Task.objects.filter(is_completed=False, due_date__lt=now.date()).count()
    task_completion_rate = round((tasks_completed / tasks_total * 100), 1) if tasks_total > 0 else 0

    leads_by_status = list(LeadStatus.objects.filter(is_active=True).annotate(count=Count('lead')).order_by('-count'))
    leads_by_source = list(LeadSource.objects.filter(is_active=True).annotate(count=Count('lead')).order_by('-count'))
    opps_by_stage = list(OpportunityStage.objects.filter(is_active=True).annotate(count=Count('stage_opportunities'), total_value=Sum('stage_opportunities__estimated_value')).order_by('order'))
    properties_by_type = list(PropertyType.objects.annotate(count=Count('property')).order_by('-count'))
    tasks_by_priority = list(TaskPriority.objects.annotate(count=Count('task')).order_by('-count'))

    max_lead_status = max((s.count for s in leads_by_status), default=1) or 1
    max_lead_source = max((s.count for s in leads_by_source), default=1) or 1
    max_opp_stage = max((s.count for s in opps_by_stage), default=1) or 1
    max_prop_type = max((t.count for t in properties_by_type), default=1) or 1
    max_task_priority = max((p.count for p in tasks_by_priority), default=1) or 1

    context = {
        'leads_this_month': leads_this_month,
        'leads_this_week': leads_this_week,
        'total_leads': total_leads,
        'total_properties': total_properties,
        'properties_value': properties_value,
        'total_opps': total_opps,
        'total_value': total_value,
        'won_opps': won_opps,
        'won_value': won_value,
        'lost_opps': lost_opps,
        'win_rate': win_rate,
        'tasks_total': tasks_total,
        'tasks_completed': tasks_completed,
        'tasks_overdue': tasks_overdue,
        'task_completion_rate': task_completion_rate,
        'leads_by_status': leads_by_status,
        'leads_by_source': leads_by_source,
        'opps_by_stage': opps_by_stage,
        'properties_by_type': properties_by_type,
        'tasks_by_priority': tasks_by_priority,
        'max_lead_status': max_lead_status,
        'max_lead_source': max_lead_source,
        'max_opp_stage': max_opp_stage,
        'max_prop_type': max_prop_type,
        'max_task_priority': max_task_priority,
    }
    return render(request, 'reports/reports_dashboard.html', context)


@login_required
def report_leads(request):
    leads = Lead.objects.select_related('source', 'status', 'assigned_to').all()
    status_id = request.GET.get('status', '')
    source_id = request.GET.get('source', '')
    priority = request.GET.get('priority', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if status_id:
        leads = leads.filter(status_id=status_id)
    if source_id:
        leads = leads.filter(source_id=source_id)
    if priority:
        leads = leads.filter(priority=priority)
    if date_from:
        leads = leads.filter(created_at__date__gte=date_from)
    if date_to:
        leads = leads.filter(created_at__date__lte=date_to)

    total = leads.count()
    by_status = list(LeadStatus.objects.filter(is_active=True).annotate(count=Count('lead')).order_by('-count'))
    by_source = list(LeadSource.objects.filter(is_active=True).annotate(count=Count('lead')).order_by('-count'))
    by_priority = leads.values('priority').annotate(count=Count('id')).order_by('-count')
    by_agent = list(User.objects.filter(assigned_leads__isnull=False).annotate(count=Count('assigned_leads')).order_by('-count')[:10])

    max_status = max((s.count for s in by_status), default=1) or 1
    max_source = max((s.count for s in by_source), default=1) or 1
    max_agent = max((a.count for a in by_agent), default=1) or 1

    context = {
        'leads': leads[:50],
        'total': total,
        'statuses': LeadStatus.objects.filter(is_active=True),
        'sources': LeadSource.objects.filter(is_active=True),
        'by_status': by_status,
        'by_source': by_source,
        'by_priority': by_priority,
        'by_agent': by_agent,
        'max_status': max_status,
        'max_source': max_source,
        'max_agent': max_agent,
        'selected_status': status_id,
        'selected_source': source_id,
        'selected_priority': priority,
    }
    return render(request, 'reports/report_leads.html', context)


@login_required
def report_properties(request):
    properties = Property.objects.filter(is_active=True).select_related('property_type', 'status', 'listed_by')
    city = request.GET.get('city', '')
    prop_type = request.GET.get('type', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if city:
        properties = properties.filter(city__icontains=city)
    if prop_type:
        properties = properties.filter(property_type_id=prop_type)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)

    total = properties.count()
    total_value = properties.aggregate(total=Sum('price'))['total'] or 0
    avg_price = properties.aggregate(avg=Avg('price'))['avg'] or 0

    by_type = list(PropertyType.objects.annotate(count=Count('property'), total_value=Sum('property__price')).order_by('-count'))
    by_status = list(PropertyStatus.objects.annotate(count=Count('property')).order_by('-count'))
    by_city = list(properties.values('city').annotate(count=Count('id'), avg_price=Avg('price')).order_by('-count')[:10])

    price_ranges = [
        ('Under $100K', 0, 100000),
        ('$100K - $250K', 100000, 250000),
        ('$250K - $500K', 250000, 500000),
        ('$500K - $1M', 500000, 1000000),
        ('$1M+', 1000000, 999999999),
    ]
    price_distribution = []
    for label, low, high in price_ranges:
        count = properties.filter(price__gte=low, price__lt=high).count()
        price_distribution.append({'label': label, 'count': count})

    features = {
        'garage': properties.filter(has_garage=True).count(),
        'pool': properties.filter(has_pool=True).count(),
        'garden': properties.filter(has_garden=True).count(),
        'pet_friendly': properties.filter(pet_friendly=True).count(),
        'featured': properties.filter(is_featured=True).count(),
    }

    max_type = max((t.count for t in by_type), default=1) or 1
    max_city = max((c['count'] for c in by_city), default=1) or 1
    max_price_range = max((p['count'] for p in price_distribution), default=1) or 1

    context = {
        'properties': properties[:50],
        'total': total,
        'total_value': total_value,
        'avg_price': avg_price,
        'types': PropertyType.objects.all(),
        'by_type': by_type,
        'by_status': by_status,
        'by_city': by_city,
        'price_distribution': price_distribution,
        'features': features,
        'max_type': max_type,
        'max_city': max_city,
        'max_price_range': max_price_range,
    }
    return render(request, 'reports/report_properties.html', context)


@login_required
def report_opportunities(request):
    opportunities = Opportunity.objects.filter(is_active=True).select_related('stage', 'lead', 'related_property', 'assigned_to')
    stage_id = request.GET.get('stage', '')
    opp_type = request.GET.get('type', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if stage_id:
        opportunities = opportunities.filter(stage_id=stage_id)
    if opp_type:
        opportunities = opportunities.filter(opportunity_type=opp_type)
    if date_from:
        opportunities = opportunities.filter(created_at__date__gte=date_from)
    if date_to:
        opportunities = opportunities.filter(created_at__date__lte=date_to)

    total = opportunities.count()
    total_value = opportunities.aggregate(total=Sum('estimated_value'))['total'] or 0
    won = opportunities.filter(actual_close_date__isnull=False)
    won_count = won.count()
    won_value = won.aggregate(total=Sum('estimated_value'))['total'] or 0
    lost_count = total - won_count
    win_rate = round((won_count / total * 100), 1) if total > 0 else 0

    by_stage = list(OpportunityStage.objects.filter(is_active=True).annotate(
        count=Count('stage_opportunities'), total_value=Sum('stage_opportunities__estimated_value')
    ).order_by('order'))
    by_type = list(opportunities.values('opportunity_type').annotate(count=Count('id'), total_value=Sum('estimated_value')).order_by('-count'))
    by_agent = list(User.objects.filter(assigned_opportunities__isnull=False).annotate(
        count=Count('assigned_opportunities'), total_value=Sum('assigned_opportunities__estimated_value')
    ).order_by('-count')[:10])

    monthly = list(
        opportunities.annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'), total_value=Sum('estimated_value'))
        .order_by('-month')[:12]
    )
    monthly.reverse()

    max_stage = max((s.count for s in by_stage), default=1) or 1
    max_agent = max((a.count for a in by_agent), default=1) or 1
    max_monthly = max((m['count'] for m in monthly), default=1) or 1

    context = {
        'opportunities': opportunities[:50],
        'total': total,
        'total_value': total_value,
        'won_count': won_count,
        'won_value': won_value,
        'lost_count': lost_count,
        'win_rate': win_rate,
        'stages': OpportunityStage.objects.filter(is_active=True),
        'by_stage': by_stage,
        'by_type': by_type,
        'by_agent': by_agent,
        'monthly': monthly,
        'max_stage': max_stage,
        'max_agent': max_agent,
        'max_monthly': max_monthly,
    }
    return render(request, 'reports/report_opportunities.html', context)


@login_required
def report_tasks(request):
    tasks = Task.objects.select_related('category', 'priority', 'status', 'assigned_to').all()
    status_id = request.GET.get('status', '')
    priority_id = request.GET.get('priority', '')
    category_id = request.GET.get('category', '')

    if status_id:
        tasks = tasks.filter(status_id=status_id)
    if priority_id:
        tasks = tasks.filter(priority_id=priority_id)
    if category_id:
        tasks = tasks.filter(category_id=category_id)

    total = tasks.count()
    completed = tasks.filter(is_completed=True).count()
    pending = tasks.filter(is_completed=False).count()
    overdue = tasks.filter(is_completed=False, due_date__lt=timezone.now().date()).count()
    completion_rate = round((completed / total * 100), 1) if total > 0 else 0

    by_status = list(TaskStatus.objects.annotate(count=Count('task')).order_by('-count'))
    by_priority = list(TaskPriority.objects.annotate(count=Count('task')).order_by('-count'))
    by_category = list(TaskCategory.objects.annotate(count=Count('task')).order_by('-count'))
    by_agent = list(User.objects.filter(assigned_tasks__isnull=False).annotate(
        count=Count('assigned_tasks'),
        completed=Count('assigned_tasks', filter=Q(assigned_tasks__is_completed=True))
    ).order_by('-count')[:10])

    max_status = max((s.count for s in by_status), default=1) or 1
    max_priority = max((p.count for p in by_priority), default=1) or 1
    max_category = max((c.count for c in by_category), default=1) or 1
    max_agent = max((a.count for a in by_agent), default=1) or 1

    context = {
        'tasks': tasks[:50],
        'total': total,
        'completed': completed,
        'pending': pending,
        'overdue': overdue,
        'completion_rate': completion_rate,
        'statuses': TaskStatus.objects.all(),
        'priorities': TaskPriority.objects.all(),
        'categories': TaskCategory.objects.all(),
        'by_status': by_status,
        'by_priority': by_priority,
        'by_category': by_category,
        'by_agent': by_agent,
        'max_status': max_status,
        'max_priority': max_priority,
        'max_category': max_category,
        'max_agent': max_agent,
    }
    return render(request, 'reports/report_tasks.html', context)


@login_required
def report_agents(request):
    agents = User.objects.filter(is_active=True).annotate(
        lead_count=Count('assigned_leads'),
        property_count=Count('listed_properties'),
        opp_count=Count('assigned_opportunities'),
        opp_value=Sum('assigned_opportunities__estimated_value'),
        task_count=Count('assigned_tasks'),
        tasks_completed=Count('assigned_tasks', filter=Q(assigned_tasks__is_completed=True)),
    ).order_by('-lead_count')

    total_leads = Lead.objects.count()
    total_opps = Opportunity.objects.filter(is_active=True).count()
    total_tasks = Task.objects.count()

    context = {
        'agents': agents,
        'total_leads': total_leads,
        'total_opps': total_opps,
        'total_tasks': total_tasks,
    }
    return render(request, 'reports/report_agents.html', context)


@login_required
def report_pipeline(request):
    stages = OpportunityStage.objects.filter(is_active=True).annotate(
        count=Count('stage_opportunities'),
        total_value=Sum('stage_opportunities__estimated_value'),
        avg_value=Avg('stage_opportunities__estimated_value'),
    ).order_by('order')

    total_opps = Opportunity.objects.filter(is_active=True).count()
    total_value = Opportunity.objects.filter(is_active=True).aggregate(total=Sum('estimated_value'))['total'] or 0

    max_count = max((s.count for s in stages), default=1) or 1

    context = {
        'stages': stages,
        'total_opps': total_opps,
        'total_value': total_value,
        'max_count': max_count,
    }
    return render(request, 'reports/report_pipeline.html', context)


@login_required
def report_revenue(request):
    now = timezone.now()
    monthly = list(
        Opportunity.objects.filter(is_active=True, actual_close_date__isnull=False)
        .annotate(month=TruncMonth('actual_close_date'))
        .values('month')
        .annotate(count=Count('id'), total_value=Sum('estimated_value'))
        .order_by('-month')[:12]
    )
    monthly.reverse()

    by_type = list(
        Opportunity.objects.filter(is_active=True, actual_close_date__isnull=False)
        .values('opportunity_type')
        .annotate(count=Count('id'), total_value=Sum('estimated_value'))
        .order_by('-total_value')
    )

    total_revenue = sum(m['total_value'] for m in monthly)
    total_deals = sum(m['count'] for m in monthly)
    avg_deal = round(total_revenue / total_deals, 2) if total_deals > 0 else 0

    max_monthly = max((m['total_value'] for m in monthly), default=1) or 1

    context = {
        'monthly': monthly,
        'by_type': by_type,
        'total_revenue': total_revenue,
        'total_deals': total_deals,
        'avg_deal': avg_deal,
        'max_monthly': max_monthly,
    }
    return render(request, 'reports/report_revenue.html', context)
