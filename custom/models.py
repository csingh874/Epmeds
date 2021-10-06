from django.db import models
from django.contrib.auth.models import AbstractUser


def get_default_id():
    pass
    # data = CustomUser.objects.order_by('-id')
    # return data[0].id + 1 if data else 1


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, blank=True, unique=True)
    rec_date = models.DateField(blank=True, null=True)
    account = models.CharField(max_length=250, default=get_default_id, blank=True, null=True)
    middle_initiative = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=10, blank=True, null=True)
    telephone = models.CharField(max_length=13, blank=True, null=True)
    speciality = models.CharField(max_length=12, choices=(('physician', 'Physician'), ('dentist', 'Dentist')),
                                  blank=True, null=True)
    dr_grp = models.CharField(max_length=50, blank=True, null=True)
    telephone2 = models.CharField(max_length=13, blank=True, null=True)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    city2 = models.CharField(max_length=50, blank=True, null=True)
    state2 = models.CharField(max_length=50, blank=True, null=True)
    zip_code2 = models.CharField(max_length=10, blank=True, null=True)
