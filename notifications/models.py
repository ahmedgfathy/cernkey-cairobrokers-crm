from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class NotificationType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#dc3545')
    icon = models.CharField(max_length=50, default='bell')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'notifications_notification_type'


class Notification(models.Model):
    NOTIFICATION_PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')

    title = models.CharField(max_length=200)
    message = models.TextField()

    notification_type = models.ForeignKey(NotificationType, on_delete=models.SET_NULL, null=True)
    priority = models.CharField(max_length=10, choices=NOTIFICATION_PRIORITY_CHOICES, default='medium')

    # Related objects stored as generic references to avoid circular imports
    related_lead_id = models.PositiveIntegerField(null=True, blank=True)
    related_property_id = models.PositiveIntegerField(null=True, blank=True)
    related_opportunity_id = models.PositiveIntegerField(null=True, blank=True)
    related_task_id = models.PositiveIntegerField(null=True, blank=True)

    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.recipient.username}"

    class Meta:
        db_table = 'notifications_notification'
        ordering = ['-created_at']
