from django.contrib import admin
from .models import Opportunity, OpportunityStage


@admin.register(OpportunityStage)
class OpportunityStageAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'probability', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('order',)


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'lead', 'related_property', 'opportunity_type', 'stage', 'assigned_to', 'estimated_value', 'expected_close_date', 'probability', 'is_active')
    list_filter = ('opportunity_type', 'stage', 'assigned_to', 'is_active', 'created_at')
    search_fields = ('name', 'lead__first_name', 'lead__last_name', 'related_property__title')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Opportunity Information', {
            'fields': ('name', 'description', 'opportunity_type')
        }),
        ('Related Objects', {
            'fields': ('lead', 'related_property')
        }),
        ('Sales Process', {
            'fields': ('stage', 'assigned_to', 'probability')
        }),
        ('Financial Details', {
            'fields': ('estimated_value', 'expected_close_date', 'actual_close_date')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at', 'is_active'),
            'classes': ('collapse',)
        }),
    )
