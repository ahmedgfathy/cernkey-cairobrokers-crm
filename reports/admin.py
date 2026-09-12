from django.contrib import admin
from .models import Report, ReportType


@admin.register(ReportType)
class ReportTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_type', 'format', 'generated_by', 'generated_at')
    list_filter = ('report_type', 'format', 'generated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('generated_at',)
