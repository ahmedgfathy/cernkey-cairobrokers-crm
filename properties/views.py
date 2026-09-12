from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Property, PropertyType, PropertyStatus
from .forms import PropertyForm, PropertyTypeForm, PropertyStatusForm, PropertySearchForm


@login_required
def property_list(request):
    properties = Property.objects.filter(is_active=True)
    search_form = PropertySearchForm(request.GET)

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        min_price = search_form.cleaned_data.get('min_price')
        max_price = search_form.cleaned_data.get('max_price')
        bedrooms = search_form.cleaned_data.get('bedrooms')
        city = search_form.cleaned_data.get('city')

        if query:
            properties = properties.filter(
                Q(title__icontains=query) | Q(address__icontains=query) |
                Q(city__icontains=query) | Q(description__icontains=query)
            )
        if min_price:
            properties = properties.filter(price__gte=min_price)
        if max_price:
            properties = properties.filter(price__lte=max_price)
        if bedrooms:
            properties = properties.filter(bedrooms__gte=bedrooms)
        if city:
            properties = properties.filter(city__icontains=city)

    context = {
        'properties': properties,
        'search_form': search_form,
    }
    return render(request, 'properties/property_list.html', context)


@login_required
def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    return render(request, 'properties/property_detail.html', {'property': property_obj})


@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.listed_by = request.user
            prop.save()
            messages.success(request, 'Property created successfully.')
            return redirect('property_detail', pk=prop.pk)
    else:
        form = PropertyForm()
    return render(request, 'properties/property_form.html', {'form': form, 'action': 'Create'})


@login_required
def property_update(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully.')
            return redirect('property_detail', pk=property_obj.pk)
    else:
        form = PropertyForm(instance=property_obj)
    return render(request, 'properties/property_form.html', {'form': form, 'action': 'Update', 'property': property_obj})


@login_required
def property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'Property deleted successfully.')
        return redirect('property_list')
    return render(request, 'properties/property_confirm_delete.html', {'property': property_obj})


@login_required
def property_type_list(request):
    types = PropertyType.objects.all()
    return render(request, 'properties/property_type_list.html', {'types': types})


@login_required
def property_type_create(request):
    if request.method == 'POST':
        form = PropertyTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property type created successfully.')
            return redirect('property_type_list')
    else:
        form = PropertyTypeForm()
    return render(request, 'properties/property_type_form.html', {'form': form})


@login_required
def property_type_update(request, pk):
    ptype = get_object_or_404(PropertyType, pk=pk)
    if request.method == 'POST':
        form = PropertyTypeForm(request.POST, instance=ptype)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property type updated successfully.')
            return redirect('property_type_list')
    else:
        form = PropertyTypeForm(instance=ptype)
    return render(request, 'properties/property_type_form.html', {'form': form, 'ptype': ptype})


@login_required
def property_type_delete(request, pk):
    ptype = get_object_or_404(PropertyType, pk=pk)
    if request.method == 'POST':
        ptype.delete()
        messages.success(request, 'Property type deleted successfully.')
        return redirect('property_type_list')
    return render(request, 'properties/property_type_confirm_delete.html', {'ptype': ptype})


@login_required
def property_status_list(request):
    statuses = PropertyStatus.objects.all()
    return render(request, 'properties/property_status_list.html', {'statuses': statuses})


@login_required
def property_status_create(request):
    if request.method == 'POST':
        form = PropertyStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property status created successfully.')
            return redirect('property_status_list')
    else:
        form = PropertyStatusForm()
    return render(request, 'properties/property_status_form.html', {'form': form})


@login_required
def property_status_update(request, pk):
    pstatus = get_object_or_404(PropertyStatus, pk=pk)
    if request.method == 'POST':
        form = PropertyStatusForm(request.POST, instance=pstatus)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property status updated successfully.')
            return redirect('property_status_list')
    else:
        form = PropertyStatusForm(instance=pstatus)
    return render(request, 'properties/property_status_form.html', {'form': form, 'pstatus': pstatus})


@login_required
def property_status_delete(request, pk):
    pstatus = get_object_or_404(PropertyStatus, pk=pk)
    if request.method == 'POST':
        pstatus.delete()
        messages.success(request, 'Property status deleted successfully.')
        return redirect('property_status_list')
    return render(request, 'properties/property_status_confirm_delete.html', {'pstatus': pstatus})
