from django.db import models
from django.contrib.auth import get_user_model

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

    def __str__(self):
        return f"{self.title} - {self.address}"

    @property
    def full_address(self):
        return f"{self.address}, {self.city}, {self.state} {self.zip_code}"

    class Meta:
        db_table = 'properties_property'
        ordering = ['-created_at']
