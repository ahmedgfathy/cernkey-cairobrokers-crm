from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Document, DocumentType
from .forms import DocumentForm, DocumentTypeForm


@login_required
def document_list(request):
    documents = Document.objects.all()
    type_id = request.GET.get('type', '')
    if type_id:
        documents = documents.filter(document_type_id=type_id)

    context = {
        'documents': documents,
        'document_types': DocumentType.objects.filter(is_active=True),
        'selected_type': type_id,
    }
    return render(request, 'documents/document_list.html', context)


@login_required
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return render(request, 'documents/document_detail.html', {'document': document})


@login_required
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user
            if doc.file:
                doc.file_size = doc.file.size
            doc.save()
            messages.success(request, 'Document uploaded successfully.')
            return redirect('document_detail', pk=doc.pk)
    else:
        form = DocumentForm()
    return render(request, 'documents/document_form.html', {'form': form, 'action': 'Upload'})


@login_required
def document_update(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.version += 1
            if doc.file:
                doc.file_size = doc.file.size
            doc.save()
            messages.success(request, 'Document updated successfully.')
            return redirect('document_detail', pk=doc.pk)
    else:
        form = DocumentForm(instance=document)
    return render(request, 'documents/document_form.html', {'form': form, 'action': 'Update', 'document': document})


@login_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document deleted successfully.')
        return redirect('document_list')
    return render(request, 'documents/document_confirm_delete.html', {'document': document})


@login_required
def document_type_list(request):
    types = DocumentType.objects.all()
    return render(request, 'documents/document_type_list.html', {'types': types})


@login_required
def document_type_create(request):
    if request.method == 'POST':
        form = DocumentTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document type created successfully.')
            return redirect('document_type_list')
    else:
        form = DocumentTypeForm()
    return render(request, 'documents/document_type_form.html', {'form': form})


@login_required
def document_type_update(request, pk):
    dtype = get_object_or_404(DocumentType, pk=pk)
    if request.method == 'POST':
        form = DocumentTypeForm(request.POST, instance=dtype)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document type updated successfully.')
            return redirect('document_type_list')
    else:
        form = DocumentTypeForm(instance=dtype)
    return render(request, 'documents/document_type_form.html', {'form': form, 'dtype': dtype})


@login_required
def document_type_delete(request, pk):
    dtype = get_object_or_404(DocumentType, pk=pk)
    if request.method == 'POST':
        dtype.delete()
        messages.success(request, 'Document type deleted successfully.')
        return redirect('document_type_list')
    return render(request, 'documents/document_type_confirm_delete.html', {'dtype': dtype})
