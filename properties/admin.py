from django.contrib import admin
from .models import Property, PropertyType, PropertyStatus

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(PropertyStatus)
class PropertyStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'state', 'price', 'bedrooms', 'bathrooms', 'square_feet', 'status', 'is_active', 'listed_by')
    list_filter = ('property_type', 'status', 'city', 'state', 'is_active', 'is_featured', 'listed_by')
    search_fields = ('title', 'address', 'city', 'state', 'zip_code')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Property Details', {
            'fields': ('property_type', 'status', 'bedrooms', 'bathrooms', 'square_feet', 'lot_size', 'year_built')
        }),
        ('Financial Information', {
            'fields': ('price', 'monthly_rent', 'hoa_fee')
        }),
        ('Features', {
            'fields': ('has_garage', 'garage_spaces', 'has_pool', 'has_garden', 'pet_friendly')
        }),
        ('Media', {
            'fields': ('main_image',)
        }),
        ('Metadata', {
            'fields': ('listed_by', 'is_featured', 'is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
