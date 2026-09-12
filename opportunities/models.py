from django.db import models
from django.contrib.auth import get_user_model
from leads.models import Lead
from properties.models import Property
from datetime import date

User = get_user_model()


class OpportunityStage(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#ffc107')
    description = models.TextField(blank=True)
    probability = models.PositiveIntegerField(default=0, help_text="Probability of closing (%)")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'opportunities_opportunity_stage'
        ordering = ['order']


class Opportunity(models.Model):
    OPPORTUNITY_TYPE_CHOICES = [
        ('sale', 'Sale'),
        ('rental', 'Rental'),
        ('lease', 'Lease'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    opportunity_type = models.CharField(max_length=20, choices=OPPORTUNITY_TYPE_CHOICES)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='opportunities')
    related_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='opportunities')

    stage = models.ForeignKey(OpportunityStage, on_delete=models.SET_NULL, null=True, blank=True, related_name='stage_opportunities')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_opportunities')

    estimated_value = models.DecimalField(max_digits=12, decimal_places=2)
    expected_close_date = models.DateField()
    actual_close_date = models.DateField(null=True, blank=True)

    probability = models.PositiveIntegerField(default=0, help_text="Probability of closing (%)")

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_opportunities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.lead.full_name}"

    @property
    def is_won(self):
        return self.actual_close_date is not None

    @property
    def days_open(self):
        return (date.today() - self.created_at.date()).days

    class Meta:
        db_table = 'opportunities_opportunity'
        ordering = ['-created_at']
