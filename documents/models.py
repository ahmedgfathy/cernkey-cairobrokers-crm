from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class DocumentType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'documents_document_type'


class Document(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    related_lead_id = models.PositiveIntegerField(null=True, blank=True)
    related_property_id = models.PositiveIntegerField(null=True, blank=True)
    related_opportunity_id = models.PositiveIntegerField(null=True, blank=True)

    document_type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='documents/')
    file_size = models.PositiveIntegerField(help_text="File size in bytes", null=True, blank=True)

    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_documents')
    is_public = models.BooleanField(default=False)
    requires_login = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    @property
    def file_extension(self):
        import os
        return os.path.splitext(self.file.name)[1]

    @property
    def file_size_mb(self):
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0

    class Meta:
        db_table = 'documents_document'
        ordering = ['-created_at']
