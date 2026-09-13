from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('leads', '0002_leadcall_leademail_leadmeeting_leadnote_leadtask'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeadSavedFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('columns', models.JSONField(default=list)),
                ('filters', models.JSONField(default=dict)),
                ('is_last_used', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lead_saved_filters', to=settings.AUTH_USER_MODEL)),
            ],
            options={'db_table': 'leads_saved_filter', 'ordering': ['name']},
        ),
        migrations.AddConstraint(
            model_name='leadsavedfilter',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_lead_saved_filter_name'),
        ),
    ]