from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import (Property, PropertyType, PropertyStatus, PropertyUnit,
                     PropertyViewing, PropertyOffer, PropertyNote)
from .forms import (PropertyForm, PropertyTypeForm, PropertyStatusForm,
                    PropertySearchForm, PropertyUnitForm, PropertyViewingForm,
                    PropertyOfferForm, PropertyNoteForm)


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
    units = property_obj.units.all()
    viewings = property_obj.viewings.all()[:10]
    offers = property_obj.offers.all()[:10]
    notes = property_obj.property_notes.all()[:10]

    all_activities = []
    for v in viewings:
        all_activities.append({'type': 'viewing', 'title': f"Viewing: {v.prospect_name}", 'date': v.viewing_date, 'status': v.get_status_display(), 'icon': 'fa-eye', 'color': '#007bff'})
    for o in offers:
        all_activities.append({'type': 'offer', 'title': f"Offer: ${o.offer_amount} from {o.buyer_name}", 'date': o.created_at, 'status': o.get_status_display(), 'icon': 'fa-handshake', 'color': '#28a745'})
    for n in notes:
        all_activities.append({'type': 'note', 'title': n.content[:80], 'date': n.created_at, 'status': 'Note', 'icon': 'fa-sticky-note', 'color': '#fd7e14'})
    all_activities.sort(key=lambda x: x['date'], reverse=True)

    context = {
        'property': property_obj,
        'units': units,
        'viewings': viewings,
        'offers': offers,
        'notes': notes,
        'all_activities': all_activities[:20],
        'unit_form': PropertyUnitForm(),
        'viewing_form': PropertyViewingForm(),
        'offer_form': PropertyOfferForm(),
        'note_form': PropertyNoteForm(),
    }
    return render(request, 'properties/property_detail.html', context)


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
def property_unit_create(request, property_pk):
    property_obj = get_object_or_404(Property, pk=property_pk)
    if request.method == 'POST':
        form = PropertyUnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.related_property = property_obj
            unit.save()
            messages.success(request, 'Unit added.')
    return redirect('property_detail', pk=property_pk)


@login_required
def property_unit_update(request, pk):
    unit = get_object_or_404(PropertyUnit, pk=pk)
    if request.method == 'POST':
        form = PropertyUnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unit updated.')
    return redirect('property_detail', pk=unit.related_property.pk)


@login_required
def property_unit_delete(request, pk):
    unit = get_object_or_404(PropertyUnit, pk=pk)
    property_pk = unit.related_property.pk
    unit.delete()
    messages.success(request, 'Unit deleted.')
    return redirect('property_detail', pk=property_pk)


@login_required
def property_viewing_create(request, property_pk):
    property_obj = get_object_or_404(Property, pk=property_pk)
    if request.method == 'POST':
        form = PropertyViewingForm(request.POST)
        if form.is_valid():
            viewing = form.save(commit=False)
            viewing.related_property = property_obj
            viewing.agent = request.user
            viewing.save()
            messages.success(request, 'Viewing scheduled.')
    return redirect('property_detail', pk=property_pk)


@login_required
def property_viewing_delete(request, pk):
    viewing = get_object_or_404(PropertyViewing, pk=pk)
    property_pk = viewing.related_property.pk
    viewing.delete()
    messages.success(request, 'Viewing deleted.')
    return redirect('property_detail', pk=property_pk)


@login_required
def property_offer_create(request, property_pk):
    property_obj = get_object_or_404(Property, pk=property_pk)
    if request.method == 'POST':
        form = PropertyOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.related_property = property_obj
            offer.agent = request.user
            offer.save()
            messages.success(request, 'Offer recorded.')
    return redirect('property_detail', pk=property_pk)


@login_required
def property_offer_update(request, pk):
    offer = get_object_or_404(PropertyOffer, pk=pk)
    if request.method == 'POST':
        form = PropertyOfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Offer updated.')
    return redirect('property_detail', pk=offer.related_property.pk)


@login_required
def property_offer_delete(request, pk):
    offer = get_object_or_404(PropertyOffer, pk=pk)
    property_pk = offer.related_property.pk
    offer.delete()
    messages.success(request, 'Offer deleted.')
    return redirect('property_detail', pk=property_pk)


@login_required
def property_note_create(request, property_pk):
    property_obj = get_object_or_404(Property, pk=property_pk)
    if request.method == 'POST':
        form = PropertyNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.related_property = property_obj
            note.created_by = request.user
            note.save()
            messages.success(request, 'Note added.')
    return redirect('property_detail', pk=property_pk)


@login_required
def property_note_delete(request, pk):
    note = get_object_or_404(PropertyNote, pk=pk)
    property_pk = note.related_property.pk
    note.delete()
    messages.success(request, 'Note deleted.')
    return redirect('property_detail', pk=property_pk)


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
