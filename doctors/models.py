from django.db import models
from patients.models import Member
from django.conf import settings


class CommunicationLog(models.Model):
    patient_id = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    doctor_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                  limit_choices_to={'groups__name': 'provider'})
    sent_by = models.CharField(max_length=3, choices=(('dr', 'Doctor'), ('pat', 'Patient')))
    messages = models.CharField(max_length=250)
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=4, choices=(('new', 'New'), ('view', 'View')), default="new")
