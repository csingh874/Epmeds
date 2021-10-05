from django.db import models
from django.db.models.fields import TextField

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import uuid
from datetime import date
from django.conf import settings


# Create your models here.
def date_validator(dob):
    if dob >= date.today():
        raise ValidationError(_('Date Should not be of Future'))
    return dob


def get_account_id():
    data = Member.objects.order_by('-id')
    return data[0].id if data else 1


class Member(models.Model):
    account = models.CharField(max_length=50, default=get_account_id, blank=True, null=False)
    idx = models.UUIDField(default=uuid.uuid4, editable=False)
    parent_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE,
                                    limit_choices_to={'groups__name': 'member'})
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    address = models.TextField(null=True, blank=True)
    address_2 = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    sex = models.CharField(max_length=7, choices=[(None, 'Please Select'), ('male', 'Male'), ('female', 'Female'),
                                                  ('unknown', 'Unknown')], default=None)
    ssn = models.CharField(max_length=10, null=True, blank=True)
    dob = models.DateField(validators=[date_validator])
    marital_status = models.CharField(max_length=20, choices=[(None, 'Please Select'), ('single', 'Single'),
                                                              ('married', 'Married'), ('widowed', 'Widowed'),
                                                              ('divorced', 'Divorced'), ('common_law', 'Common Law'),
                                                              ('legally_separated', 'Legally Separated')],
                                      default=None)
    home_phone = models.CharField(max_length=20, null=True, blank=True)
    cell_phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=50, null=False, blank=True)
    race = models.CharField(max_length=30, choices=[(None, 'Please Select'), ('white', 'White'), ('asian', 'Asian'),
                                                    ('african_american', 'African American'),
                                                    ('american_indian_alaskan', 'American Indian/Alaskan'),
                                                    ('hawaiian_pacific_islander', 'Hawaiian/Pacific Islander'),
                                                    ('other', 'Other')], default=None, blank=True, null=True)
    ethnicity = models.CharField(max_length=50, null=True, blank=True,
                                 choices=[(None, 'Please Select'), ('hispanic_latino', 'Hispanic or Latino'),
                                          ('not_hispanic_latino', 'Not Hispanic or Latino')], default=None)
    primary_language = models.CharField(max_length=100, null=True, blank=True)
    height = models.CharField(max_length=10, null=True, blank=True)
    current_weight = models.CharField(max_length=10, null=True, blank=True)
    blood_type = models.CharField(max_length=10, null=False, blank=True, choices=((None, 'Please Select'),
                                                                                  ('a_pos', 'A+'), ('a_neg', 'A-'),
                                                                                  ('ab_pos', 'AB+'), ('ab_neg', 'AB-'),
                                                                                  ('b_pos', 'B+'), ('b_neg', 'B-'),
                                                                                  ('o_pos', 'O+'), ('o_neg', 'O-')),
                                  default=None)
    spouse_name = models.CharField(max_length=50, null=True, blank=True)
    spouse_dob = models.DateField(null=True, blank=True, validators=[date_validator])

    def __str__(self):
        return f"{self.id} {self.first_name} {self.last_name}"


class EmploymentInfo(models.Model):
    member_id = models.OneToOneField(Member, on_delete=models.CASCADE, null=True, blank=True)
    work_status = models.CharField(max_length=10, choices=(('full_time', 'Full Time'), ('part_time', 'Part Time'),
                                                           ('unemployed', 'Unemployed'), ('student', 'Student'),
                                                           ('retired', 'Retired')), blank=True, null=True)
    occupation = models.CharField(max_length=50)
    employer_name = models.CharField(max_length=50, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    address1 = models.CharField(max_length=250, blank=True, null=True)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)


class AdvanceDirectives(models.Model):
    member_id = models.OneToOneField(Member, on_delete=models.CASCADE, null=True, blank=True)
    advance_dir = models.BooleanField(choices=((True, 'Yes'), (False, 'No')), blank=True, null=True)
    state_advance_dir = models.BooleanField(choices=((True, 'Yes'), (False, 'No')), blank=True, null=True)
    personal_health = models.BooleanField(choices=((True, 'Yes'), (False, 'No')), blank=True, null=True)
    upload_personal_health = models.BooleanField(choices=((True, 'Yes'), (False, 'No')), default=False,
                                                 blank=True, null=True)
    doc_file = models.FileField(upload_to='documents/%Y/%m/%d')


class EmergencyContact(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    auth_rep = models.BooleanField(choices=((True, "Yes"), (False, 'No')), default=False)
    emg_date = models.DateField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    relation = models.CharField(max_length=20)
    telephone = models.CharField(max_length=12)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)


class DoctorRole(models.Model):
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name


class MedicalProvider(models.Model):
    rec_date = models.DateField()
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    doctor_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                  limit_choices_to={'groups__name': 'provider'})
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=13)
    holders_relationship = models.ForeignKey(DoctorRole, on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.first_name


class Insurance(models.Model):
    insurance_company = models.CharField(max_length=50)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    policy_holder = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='policy_holder')
    relationship = models.CharField(max_length=15, choices=((None, 'Select Relationship'), ('self', 'Self'),
                                                            ('spouse', 'Spouse'), ('child', 'Child'),
                                                            ('parent', 'parent'), ('other', 'Other')))
    group_name = models.CharField(max_length=100)
    policy = models.CharField(max_length=50)
    telephone = models.CharField(max_length=15)
    policy_start_date = models.DateField()
    policy_end_date = models.DateField()
    comments = models.CharField(max_length=250)

    def __str__(self):
        return self.policy


class Allergies(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    no_know_allergy = models.BooleanField(default=False)
    rec_date = models.DateField()
    food_allergy = models.CharField(max_length=100, blank=True, null=True)
    drug_allergy = models.CharField(max_length=100, blank=True, null=True)
    comments = models.CharField(max_length=250, blank=True, null=True)
    allergy_type = models.CharField(max_length=10, choices=((None, "Select Alergy Type"), ('airbone', 'Airbone'),
                                                            ('food', 'Food'), ('drug', 'drug')), default=None)


class PrescribedMedicine(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    dr_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                              limit_choices_to={'groups__name': 'provider'})
    no_medication = models.BooleanField(default=False)
    drug_id = models.CharField(max_length=10)
    drug_name = models.CharField(max_length=50)
    drug_active = models.CharField(max_length=3, choices=(('yes', 'Yes'), ('no', 'No')))
    drug_form = models.CharField(max_length=50)
    drug_strength = models.CharField(max_length=50)
    directions = models.CharField(max_length=50)
    start_date = models.DateField()
    stop_date = models.DateField()
    prescribing_doctor = models.CharField(max_length=50, blank=True, null=True)
    trade_generic = models.CharField(max_length=50)
    comments = models.CharField(max_length=250)


class UnPrescribeMedicine(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    drug_date = models.DateField()
    drug_id = models.CharField(max_length=10)
    drug_name = models.CharField(max_length=50)
    generic = models.CharField(max_length=50)
    form_strength = models.CharField(max_length=50)


class Lab(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    rec_date = models.DateField()
    cpt_code = models.CharField(max_length=250)
    test_name = models.CharField(max_length=250)
    result = models.CharField(max_length=250)
    out_of_range = models.CharField(max_length=250)
    in_range = models.CharField(max_length=250)
    expected = models.CharField(max_length=250)
    flag = models.CharField(max_length=250)


class Diagnosis(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    admit_date = models.DateField()
    code_type = models.CharField(max_length=5, choices=((None, "Please Select"), ("icd9", "ICD9"), ('icd10', 'ICD10')),
                                 default=None)
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={"groups__name": 'member'})
    diagnosis_code = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    facility = models.CharField(max_length=250)


class VaccinationProcedure(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    vaccination_date = models.DateField()
    procedure = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    physician = models.CharField(max_length=255)


class FamilyHistory(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    medical_problem = models.CharField(max_length=255)
    age_started = models.CharField(max_length=255)
    relative = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255)


class SocialHistory(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    smoking = models.CharField(max_length=15, choices=(('every_day', 'Current every day smoker'),
                                                       ('some_day', 'Current some day smoker'),
                                                       ('former_smoker', 'Former smoker'), ('never', 'Never smoker'),
                                                       ('heavy_smoker', 'Heavy tobacco smoker'),
                                                       ('light_smoker', 'Light tobacco smoker')))
    alcohol = models.BooleanField(choices=((True, 'Yes'), (False, 'No')), default=False)
    caffeine = models.BooleanField(choices=((True, 'Yes'), (False, 'No')), default=False)
    drug = models.BooleanField(choices=((True, 'Yes'), (False, 'No')), default=False)
    exercise = models.CharField(max_length=10, choices=(('yes', 'Yes'), ('no', 'No'), ('sometimes', 'Sometimes')))
    comments = models.CharField(max_length=250)
    other_comments = models.CharField(max_length=250)


class MedicalNotes(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    visits = models.CharField(max_length=3, choices=(('int', 'Internal'), ('ext', 'External')))
    depart_date = models.DateField()
    time_out = models.CharField(max_length=5)
    time_in = models.CharField(max_length=5)
    total_time = models.CharField(max_length=5)
    caretaker_name = models.CharField(max_length=50)
    purpose = models.CharField(max_length=250)
    provider_name = models.CharField(max_length=20)
    telephone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    result = models.CharField(max_length=10)
    follow_up = models.CharField(max_length=100)
    notes_1 = models.CharField(max_length=100)
    notes_2 = models.CharField(max_length=100)
    send_email = models.BooleanField(default=False)
    send_text = models.BooleanField(default=False)


class MarModel(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    rec_date = models.DateField()
    caregiver_name = models.CharField(max_length=30)
    drug_id = models.CharField(max_length=30)
    drug_name = models.CharField(max_length=30)
    with_food_morning = models.CharField(max_length=5, null=True, blank=True)
    with_food_afternoon = models.CharField(max_length=5, null=True, blank=True)
    with_food_evening = models.CharField(max_length=5, null=True, blank=True)
    without_food_morning = models.CharField(max_length=5, null=True, blank=True)
    without_food_afternoon = models.CharField(max_length=5, null=True, blank=True)
    without_food_evening = models.CharField(max_length=5, null=True, blank=True)


class DrugDictionary(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField(choices=((True, 'Yes'), (False, 'No')), default=False)
    obsolete = models.BooleanField(choices=((True, 'Yes'), (False, 'No')), default=False)
    mnemonic = models.CharField(max_length=30)
    print_number = models.CharField(max_length=30)
    generic_name = models.CharField(max_length=30)
    drug_class = models.CharField(max_length=30)
    vendor_name = models.CharField(max_length=30)
    ndc_number = models.CharField(max_length=30)
    trade_number = models.CharField(max_length=30)
    drug_type = models.CharField(max_length=30)
    emr_id = models.CharField(max_length=30)
    vendor_mnemonic = models.CharField(max_length=30)
    usage_type = models.CharField(max_length=30, choices=(('formal', 'Formulary'), ('non-formal', 'Non-Formulary')))


class VendorDictionary(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField(choices=((True, 'Yes'), (False, 'No')), default=False)
    mnemonic = models.CharField(max_length=30)
    contact_name = models.CharField(max_length=30)
    vendor_name = models.CharField(max_length=30)
    telephone = models.CharField(max_length=15)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)


class MemberLogs(models.Model):
    access_by = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=10)
    data_access = models.CharField(max_length=50)
