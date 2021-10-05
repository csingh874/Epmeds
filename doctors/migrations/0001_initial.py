# Generated by Django 3.2.7 on 2021-10-04 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunicationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_by', models.CharField(choices=[('dr', 'Doctor'), ('pat', 'Patient')], max_length=3)),
                ('messages', models.CharField(max_length=250)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('new', 'New'), ('view', 'View')], default='new', max_length=4)),
                ('doctor_id', models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'provider'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('patient_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patients.member')),
            ],
        ),
    ]
