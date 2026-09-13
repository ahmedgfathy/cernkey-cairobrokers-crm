from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import (Property, PropertyType, PropertyStatus, PropertyUnit,
                     PropertyViewing, PropertyOffer, PropertyNote)
from .forms import (PropertyForm, PropertyTypeForm, PropertyStatusForm,
                    PropertySearchForm, PropertyUnitForm, PropertyViewingForm,
                    PropertyOfferForm, PropertyNoteForm)
from core.import_export import (export_csv, export_excel, parse_uploaded_file,
                                auto_match_headers, store_import_data,
                                load_import_data, clear_import_data)


@login_required
def property_list(request):
    properties = Property.objects.filter(is_active=True)
    search_form = PropertySearchForm(request.GET)
    per_page = request.GET.get('per_page', '25')

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

    properties = properties.select_related('property_type', 'status', 'listed_by').order_by('-created_at')

    try:
        per_page = int(per_page)
        if per_page not in [10, 25, 50, 100]:
            per_page = 25
    except (ValueError, TypeError):
        per_page = 25

    paginator = Paginator(properties, per_page)
    page_number = request.GET.get('page', '1')
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'properties': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'search_form': search_form,
        'per_page': per_page,
        'prev_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
        'page_sizes': [10, 25, 50, 100],
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


PROPERTY_EXPORT_FIELDS = [
    'title', 'description', 'address', 'city', 'state', 'zip_code', 'country',
    'property_type__name', 'status__name',
    'bedrooms', 'bathrooms', 'square_feet', 'lot_size', 'year_built',
    'price', 'monthly_rent', 'hoa_fee',
    'has_garage', 'garage_spaces', 'has_pool', 'has_garden', 'pet_friendly',
    'listed_by__first_name', 'is_featured', 'created_at',
]
PROPERTY_EXPORT_HEADERS = [
    'Title', 'Description', 'Address', 'City', 'State', 'Zip Code', 'Country',
    'Property Type', 'Status',
    'Bedrooms', 'Bathrooms', 'Square Feet', 'Lot Size', 'Year Built',
    'Price', 'Monthly Rent', 'HOA Fee',
    'Has Garage', 'Garage Spaces', 'Has Pool', 'Has Garden', 'Pet Friendly',
    'Listed By', 'Featured', 'Created At',
]
PROPERTY_DB_FIELDS = {
    'title': 'Title',
    'description': 'Description',
    'address': 'Address',
    'city': 'City',
    'state': 'State',
    'zip_code': 'Zip Code',
    'country': 'Country',
    'property_type': 'Property Type',
    'status': 'Status',
    'bedrooms': 'Bedrooms',
    'bathrooms': 'Bathrooms',
    'square_feet': 'Square Feet',
    'lot_size': 'Lot Size',
    'year_built': 'Year Built',
    'price': 'Price',
    'monthly_rent': 'Monthly Rent',
    'hoa_fee': 'HOA Fee',
    'has_garage': 'Has Garage',
    'garage_spaces': 'Garage Spaces',
    'has_pool': 'Has Pool',
    'has_garden': 'Has Garden',
    'pet_friendly': 'Pet Friendly',
    'listed_by': 'Listed By',
    'is_featured': 'Featured',
    # Legacy Property.csv fields. Existing CRM fields above retain their
    # normalized meanings (Type, Total Price, Description, STATUS).
    'listing_purpose': 'Unit For',
    'property_number': 'Property Number',
    'area': 'Area',
    'unit_license': 'UNIT LICENSE',
    'phase': 'Phase',
    'community_name': 'COMMUNITY NAME',
    'mall_name': 'MALL NAME',
    'view_me': 'VIEW ME',
    'call_made_date': 'date call make',
    'finishing': 'Finished',
    'building': 'Building',
    'space_m': 'SPACE \\ M',
    'unit_number': 'Unit NO',
    'property_offered_by': 'Property Offered By',
    'update_4': '4 UBDATE',
    'contact_name': 'Name',
    'updated_by_name': 'UBDATE BY',
    'mobile_no': 'Mobile No.',
    'last_follow_in': 'Last Follow in',
    'telephone': 'Tel',
    'call_update': 'ابديت المكالمات',
    'call_note': 'NOTE OF CALL',
    'feedback': 'NEW FEEDBACK',
    'last_call_date': 'DATE OF LAST CALL',
    'more_units': 'MORE UINITS',
    'rent_to': 'Rent To',
    'reminder_time': 'RIMINDER TIME',
    'duplicate_note': 'البيان مكرر',
    'reminder_date': 'RIMINDER DATE',
    'compound_name': 'Property Name - Compound Name',
    'handler': 'Handler',
    'area_label': 'AREA LABLE',
    'legacy_modified_time': 'Modified Time',
    'legacy_created_time': 'Created Time',
    'land_area': 'Land area',
    'floors': 'The Floors',
    'business_activity': 'النشاط',
    'category': 'catogry',
    'compound_location': 'داخل كمبوند / خارج كمبوند',
    'send_a_message': 'SEND A MESSAGE',
    'sales': 'Sales',
    'last_modified_by_name': 'Last Modified By',
}

PROPERTY_LEGACY_FIELDS = (
    'listing_purpose', 'property_number', 'area', 'unit_license', 'phase',
    'community_name', 'mall_name', 'view_me', 'call_made_date', 'finishing',
    'building', 'space_m', 'unit_number', 'property_offered_by', 'update_4',
    'contact_name', 'updated_by_name', 'mobile_no', 'last_follow_in',
    'telephone', 'call_update', 'call_note', 'feedback', 'last_call_date',
    'more_units', 'rent_to', 'reminder_time', 'duplicate_note', 'reminder_date',
    'compound_name', 'handler', 'area_label', 'legacy_modified_time',
    'legacy_created_time', 'land_area', 'floors', 'business_activity', 'category',
    'compound_location', 'send_a_message', 'sales', 'last_modified_by_name',
)


@login_required
def property_export_csv(request):
    properties = Property.objects.select_related('property_type', 'status', 'listed_by').all()
    return export_csv(properties, PROPERTY_EXPORT_FIELDS, PROPERTY_EXPORT_HEADERS, 'properties_export')


@login_required
def property_export_excel(request):
    properties = Property.objects.select_related('property_type', 'status', 'listed_by').all()
    return export_excel(properties, PROPERTY_EXPORT_FIELDS, PROPERTY_EXPORT_HEADERS, 'properties_export')


@login_required
@ensure_csrf_cookie
def property_import(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            try:
                headers, rows = parse_uploaded_file(file)
            except (OSError, ValueError, ImportError) as exc:
                messages.error(request, f'Could not read this file: {exc}')
                return redirect('property_import')
            if not headers:
                messages.error(request, 'Could not parse the uploaded file. Add a header row and at least one data row.')
                return redirect('property_import')
            auto_map = auto_match_headers(headers, PROPERTY_DB_FIELDS)
            store_import_data(request, 'properties', headers, rows)
            request.session['property_import_auto_map'] = {str(k): v for k, v in auto_map.items()}
            return redirect('property_import_map')
        elif 'confirm' in request.POST:
            mapping = {}
            for idx_str, field in request.POST.items():
                if idx_str.startswith('col_') and field:
                    try:
                        idx = int(idx_str.replace('col_', ''))
                    except ValueError:
                        continue
                    if field in PROPERTY_DB_FIELDS:
                        mapping[idx] = field
            headers, rows = load_import_data(request, 'properties')
            if not headers or not rows:
                messages.error(request, 'This import session has expired. Upload the file again.')
                return redirect('property_import')
            created = 0
            updated = 0
            skipped = 0
            errors = []
            for row_idx, row in enumerate(rows):
                data = {}
                for idx, field in mapping.items():
                    if idx < len(row):
                        data[field] = str(row[idx]).strip()
                if not any(data.values()):
                    skipped += 1
                    continue
                prop_data = {field: data.get(field, '') for field in (
                    'title', 'description', 'address', 'city', 'state', 'zip_code', 'country'
                )}
                for field in PROPERTY_LEGACY_FIELDS:
                    prop_data[field] = data.get(field, '')
                prop_data['title'] = (
                    prop_data['title'].strip() or prop_data['compound_name'].strip() or
                    prop_data['property_number'].strip() or 'Untitled property'
                )
                prop_data['description'] = prop_data['description'] or 'No description'
                prop_data['country'] = prop_data['country'] or 'USA'
                for field, default in (
                    ('bedrooms', 1), ('bathrooms', 1), ('square_feet', 1000),
                    ('price', 0),
                ):
                    try:
                        prop_data[field] = int(data.get(field) or default)
                    except (TypeError, ValueError):
                        prop_data[field] = default
                if data.get('space_m') and not data.get('square_feet'):
                    digits = ''.join(char for char in data['space_m'] if char.isdigit())
                    if digits:
                        prop_data['square_feet'] = int(digits)
                for field in ('price', 'lot_size', 'monthly_rent', 'hoa_fee'):
                    if data.get(field):
                        try:
                            # Legacy prices commonly include thousands separators.
                            prop_data[field] = float(str(data[field]).replace(',', '').strip())
                        except (TypeError, ValueError):
                            errors.append(f'Row {row_idx + 2}: invalid {PROPERTY_DB_FIELDS[field]}')
                if data.get('year_built'):
                    try: prop_data['year_built'] = int(data['year_built'])
                    except (TypeError, ValueError): errors.append(f'Row {row_idx + 2}: invalid Year Built')
                if data.get('garage_spaces'):
                    try: prop_data['garage_spaces'] = int(data['garage_spaces'])
                    except (TypeError, ValueError): errors.append(f'Row {row_idx + 2}: invalid Garage Spaces')
                for bool_field in ['has_garage', 'has_pool', 'has_garden', 'pet_friendly', 'is_featured']:
                    if data.get(bool_field):
                        val = data[bool_field].strip().lower()
                        prop_data[bool_field] = val in ['yes', 'true', '1', 'on']
                if data.get('property_type'):
                    type_name = data['property_type'].strip()
                    ptype = PropertyType.objects.filter(name__iexact=type_name).first()
                    prop_data['property_type'] = ptype or PropertyType.objects.create(name=type_name)
                if data.get('status'):
                    status_name = data['status'].strip()
                    pstatus = PropertyStatus.objects.filter(name__iexact=status_name).first()
                    prop_data['status'] = pstatus or PropertyStatus.objects.create(name=status_name)
                if data.get('listed_by'):
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    agent = User.objects.filter(
                        Q(first_name__icontains=data['listed_by'].strip()) |
                        Q(last_name__icontains=data['listed_by'].strip()) |
                        Q(username__iexact=data['listed_by'].strip())
                    ).first()
                    if agent:
                        prop_data['listed_by'] = agent
                try:
                    # Legacy property numbers are the stable import identity;
                    # title remains the fallback for hand-created records.
                    if prop_data['property_number']:
                        existing = Property.objects.filter(
                            property_number__iexact=prop_data['property_number']
                        ).first()
                    else:
                        existing = Property.objects.filter(title__iexact=prop_data['title']).first()
                    if existing:
                        for k, v in prop_data.items():
                            setattr(existing, k, v)
                        existing.save()
                        updated += 1
                    else:
                        Property.objects.create(**prop_data)
                        created += 1
                except Exception as e:
                    skipped += 1
                    errors.append(f"Row {row_idx + 2}: {str(e)}")
            clear_import_data(request, 'properties')
            request.session.pop('property_import_auto_map', None)
            msg = f'Import complete: {created} created, {updated} updated, {skipped} skipped.'
            if errors:
                msg += f' {len(errors)} row errors.'
                messages.warning(request, msg)
            else:
                messages.success(request, msg)
            return redirect('property_list')
    return render(request, 'properties/property_import.html', {
        'db_fields': PROPERTY_DB_FIELDS,
    })


@login_required
def property_import_map(request):
    headers, rows = load_import_data(request, 'properties')
    auto_map = request.session.get('property_import_auto_map', {})
    if not headers:
        messages.error(request, 'No import data found. Please upload a file first.')
        return redirect('property_import')
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
    return render(request, 'properties/property_import_map.html', {
        'headers': headers,
        'preview_rows': preview_rows,
        'total_rows': len(rows),
        'auto_map': auto_map,
        'columns': columns,
        'mapped_count': len(mapped_fields - {''}),
        'unmapped_count': len(headers) - len(auto_map),
        'missing_required': [],
        'db_fields': PROPERTY_DB_FIELDS,
    })


@login_required
def property_cleanup(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'remove_duplicates':
            from django.db.models import Count
            duplicates = (
                Property.objects.values('title', 'address', 'price', 'bedrooms', 'bathrooms', 'square_feet')
                .annotate(cnt=Count('id'))
                .filter(cnt__gt=1)
            )
            removed = 0
            for dup in duplicates:
                props = Property.objects.filter(
                    title=dup['title'],
                    address=dup['address'],
                    price=dup['price'],
                    bedrooms=dup['bedrooms'],
                    bathrooms=dup['bathrooms'],
                    square_feet=dup['square_feet'],
                )
                keep = props.first()
                to_delete = props.exclude(pk=keep.pk)
                count = to_delete.count()
                to_delete.delete()
                removed += count
            messages.success(request, f'Removed {removed} duplicate properties.')
            return redirect('property_list')
        elif action == 'remove_all':
            count = Property.objects.count()
            Property.objects.all().delete()
            messages.success(request, f'Removed all {count} properties.')
            return redirect('property_list')
    from django.db.models import Count
    dups = (
        Property.objects.values('title', 'address', 'price', 'bedrooms', 'bathrooms', 'square_feet')
        .annotate(cnt=Count('id'))
        .filter(cnt__gt=1)
    )
    duplicates_count = 0
    for dup in dups:
        duplicates_count += dup['cnt'] - 1
    return render(request, 'properties/property_cleanup.html', {
        'total_properties': Property.objects.count(),
        'duplicates_count': duplicates_count,
    })
