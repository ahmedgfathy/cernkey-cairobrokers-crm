from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class PropertyType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'properties_property_type'


class PropertyStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#28a745')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'properties_property_status'


class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='USA')

    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(PropertyStatus, on_delete=models.SET_NULL, null=True, blank=True)

    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    square_feet = models.PositiveIntegerField()
    lot_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    year_built = models.PositiveIntegerField(null=True, blank=True)

    price = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hoa_fee = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    has_garage = models.BooleanField(default=False)
    garage_spaces = models.PositiveIntegerField(default=0)
    has_pool = models.BooleanField(default=False)
    has_garden = models.BooleanField(default=False)
    pet_friendly = models.BooleanField(default=False)

    main_image = models.ImageField(upload_to='property_images/', blank=True, null=True)

    listed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='listed_properties')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Legacy CRM import fields. The source file is intentionally retained in
    # full so operational history is not lost during migration to this CRM.
    listing_purpose = models.CharField(max_length=100, blank=True)
    property_number = models.CharField(max_length=50, blank=True, db_index=True)
    area = models.CharField(max_length=200, blank=True)
    unit_license = models.CharField(max_length=200, blank=True)
    phase = models.CharField(max_length=200, blank=True)
    community_name = models.CharField(max_length=250, blank=True)
    mall_name = models.CharField(max_length=250, blank=True)
    view_me = models.CharField(max_length=200, blank=True)
    call_made_date = models.CharField(max_length=100, blank=True)
    finishing = models.CharField(max_length=200, blank=True)
    building = models.CharField(max_length=200, blank=True)
    space_m = models.CharField(max_length=100, blank=True)
    unit_number = models.CharField(max_length=100, blank=True)
    property_offered_by = models.CharField(max_length=200, blank=True)
    update_4 = models.CharField(max_length=200, blank=True)
    contact_name = models.CharField(max_length=200, blank=True)
    updated_by_name = models.CharField(max_length=150, blank=True)
    mobile_no = models.CharField(max_length=50, blank=True)
    last_follow_in = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=50, blank=True)
    call_update = models.TextField(blank=True)
    call_note = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    last_call_date = models.CharField(max_length=100, blank=True)
    more_units = models.TextField(blank=True)
    rent_to = models.CharField(max_length=200, blank=True)
    reminder_time = models.CharField(max_length=100, blank=True)
    duplicate_note = models.CharField(max_length=200, blank=True)
    reminder_date = models.CharField(max_length=100, blank=True)
    compound_name = models.CharField(max_length=300, blank=True)
    handler = models.CharField(max_length=150, blank=True)
    area_label = models.CharField(max_length=200, blank=True)
    legacy_modified_time = models.CharField(max_length=100, blank=True)
    legacy_created_time = models.CharField(max_length=100, blank=True)
    land_area = models.CharField(max_length=100, blank=True)
    floors = models.TextField(blank=True)
    business_activity = models.CharField(max_length=300, blank=True)
    category = models.CharField(max_length=200, blank=True)
    compound_location = models.CharField(max_length=100, blank=True)
    send_a_message = models.CharField(max_length=100, blank=True)
    sales = models.CharField(max_length=150, blank=True)
    last_modified_by_name = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.title} - {self.address}"

    @property
    def full_address(self):
        return f"{self.address}, {self.city}, {self.state} {self.zip_code}"

    @property
    def total_units(self):
        return self.units.count()

    @property
    def available_units(self):
        return self.units.filter(status='available').count()

    class Meta:
        db_table = 'properties_property'
        ordering = ['-created_at']


class PropertyUnit(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Under Maintenance'),
    ]

    related_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units')
    unit_number = models.CharField(max_length=50)
    floor = models.CharField(max_length=20, blank=True)
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    square_feet = models.PositiveIntegerField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    description = models.TextField(blank=True)
    tenant_name = models.CharField(max_length=200, blank=True)
    tenant_phone = models.CharField(max_length=20, blank=True)
    lease_start = models.DateField(null=True, blank=True)
    lease_end = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Unit {self.unit_number} - {self.related_property.title}"

    @property
    def is_available(self):
        return self.status == 'available'

    class Meta:
        db_table = 'properties_property_unit'
        ordering = ['unit_number']
        unique_together = ['related_property', 'unit_number']


class PropertyViewing(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    related_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='viewings')
    prospect_name = models.CharField(max_length=200)
    prospect_phone = models.CharField(max_length=20, blank=True)
    prospect_email = models.EmailField(blank=True)
    viewing_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='property_viewings')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Viewing: {self.prospect_name} - {self.related_property.title}"

    class Meta:
        db_table = 'properties_property_viewing'
        ordering = ['-viewing_date']


class PropertyOffer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('countered', 'Counter Offer'),
        ('withdrawn', 'Withdrawn'),
    ]

    related_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='offers')
    buyer_name = models.CharField(max_length=200)
    buyer_phone = models.CharField(max_length=20, blank=True)
    buyer_email = models.EmailField(blank=True)
    offer_amount = models.DecimalField(max_digits=12, decimal_places=2)
    offer_date = models.DateField(default=timezone.now)
    closing_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='property_offers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"${self.offer_amount} - {self.buyer_name} for {self.related_property.title}"

    @property
    def difference_from_asking(self):
        return self.offer_amount - self.related_property.price

    class Meta:
        db_table = 'properties_property_offer'
        ordering = ['-offer_date']


class PropertyNote(models.Model):
    related_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_notes')
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note on {self.related_property}"

    class Meta:
        db_table = 'properties_property_note'
        ordering = ['-created_at']
