from django.contrib import admin
from .models import Lead, LeadSavedFilter, LeadSource, LeadStatus


@admin.register(LeadSavedFilter)
class LeadSavedFilterAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_last_used', 'updated_at')
    list_filter = ('is_last_used',)
    search_fields = ('name', 'user__username')

@admin.register(LeadSource)
class LeadSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(LeadStatus)
class LeadStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'source', 'status', 'assigned_to', 'priority', 'created_at')
    list_filter = ('source', 'status', 'priority', 'assigned_to', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'company')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'company')
        }),
        ('Lead Details', {
            'fields': ('source', 'status', 'assigned_to', 'priority')
        }),
        ('Additional Info', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )
