from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class LeadSource(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'leads_lead_source'


class LeadStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#007bff')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'leads_lead_status'


class Lead(models.Model):
    LEAD_PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=200, blank=True)

    source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(LeadStatus, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_leads')

    priority = models.CharField(max_length=10, choices=LEAD_PRIORITY_CHOICES, default='medium')
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_leads')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def activity_count(self):
        return (self.lead_tasks.count() + self.lead_calls.count() +
                self.lead_meetings.count() + self.lead_emails.count() +
                self.lead_notes.count())

    class Meta:
        db_table = 'leads_lead'
        ordering = ['-created_at']


class LeadSavedFilter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lead_saved_filters')
    name = models.CharField(max_length=100)
    columns = models.JSONField(default=list)
    filters = models.JSONField(default=dict)
    is_last_used = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.name}"

    class Meta:
        db_table = 'leads_saved_filter'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_lead_saved_filter_name'),
        ]


class LeadTask(models.Model):
    TASK_TYPE_CHOICES = [
        ('call', 'Follow-up Call'),
        ('email', 'Send Email'),
        ('meeting', 'Schedule Meeting'),
        ('viewing', 'Property Viewing'),
        ('proposal', 'Send Proposal'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='lead_tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, default='other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='lead_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.lead}"

    @property
    def is_overdue(self):
        if self.due_date and self.status != 'completed':
            return self.due_date < timezone.now().date()
        return False

    class Meta:
        db_table = 'leads_lead_task'
        ordering = ['-created_at']


class LeadCall(models.Model):
    OUTCOME_CHOICES = [
        ('connected', 'Connected'),
        ('voicemail', 'Left Voicemail'),
        ('no_answer', 'No Answer'),
        ('busy', 'Busy'),
        ('wrong_number', 'Wrong Number'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='lead_calls')
    call_date = models.DateTimeField(default=timezone.now)
    duration_minutes = models.PositiveIntegerField(default=0, help_text="Duration in minutes")
    outcome = models.CharField(max_length=20, choices=OUTCOME_CHOICES, default='connected')
    notes = models.TextField(blank=True)
    called_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='lead_calls')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Call with {self.lead} on {self.call_date}"

    class Meta:
        db_table = 'leads_lead_call'
        ordering = ['-call_date']


class LeadMeeting(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='lead_meetings')
    title = models.CharField(max_length=200)
    meeting_date = models.DateTimeField()
    location = models.CharField(max_length=300, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    organized_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='lead_meetings')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} with {self.lead}"

    class Meta:
        db_table = 'leads_lead_meeting'
        ordering = ['-meeting_date']


class LeadEmail(models.Model):
    DIRECTION_CHOICES = [
        ('outgoing', 'Sent'),
        ('incoming', 'Received'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='lead_emails')
    subject = models.CharField(max_length=300)
    body = models.TextField(blank=True)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, default='outgoing')
    sent_at = models.DateTimeField(default=timezone.now)
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='lead_emails')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.lead}"

    class Meta:
        db_table = 'leads_lead_email'
        ordering = ['-sent_at']


class LeadNote(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='lead_notes')
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note on {self.lead}"

    class Meta:
        db_table = 'leads_lead_note'
        ordering = ['-created_at']
