from django.db import models
from django.contrib.auth import get_user_model
from leads.models import Lead
from properties.models import Property
from opportunities.models import Opportunity

User = get_user_model()


class ReportType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'reports_report_type'


class Report(models.Model):
    REPORT_FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    report_type = models.ForeignKey(ReportType, on_delete=models.CASCADE, null=True, blank=True)

    parameters = models.TextField(blank=True, help_text="JSON parameters for report generation")
    format = models.CharField(max_length=10, choices=REPORT_FORMAT_CHOICES, default='pdf')

    generated_file = models.FileField(upload_to='reports/', blank=True, null=True)

    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_reports')
    generated_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'reports_report'
        ordering = ['-generated_at']
