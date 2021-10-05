from django import forms
from .models import *


class AddPatient(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'


class EmploymentInfoForm(forms.ModelForm):
    work_status = forms.ChoiceField(choices=(('full_time', 'Full Time'), ('part_time', 'Part Time'),
                                             ('unemployed', 'Unemployed'), ('student', 'Student'),
                                             ('retired', 'Retired')), widget=forms.RadioSelect, required=False)

    class Meta:
        model = EmploymentInfo
        fields = '__all__'


class AdvanceDirectiveForm(forms.ModelForm):
    advance_dir = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')), required=False, widget=forms.RadioSelect)
    state_advance_dir = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')), required=False, widget=forms.RadioSelect)
    personal_health = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')), required=False, widget=forms.RadioSelect)
    upload_personal_health = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')), required=False, widget=forms.RadioSelect)

    class Meta:
        model = AdvanceDirectives
        fields = '__all__'


class EmergencyContactForm(forms.ModelForm):
    auth_rep = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')), widget=forms.RadioSelect)

    class Meta:
        model = EmergencyContact
        fields = '__all__'


class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = '__all__'

    def clean(self):
        clean_data = self.cleaned_data
        if clean_data.get('policy_start_date') >= clean_data.get('policy_end_date'):
            raise ValidationError({'policy_start_date': 'Policy Start Date cannot be Greater then Policy End Date.'})
        return super(InsuranceForm, self).clean()


class AllergyForm(forms.ModelForm):
    class Meta:
        model = Allergies
        fields = "__all__"


class MedicineForm(forms.ModelForm):
    drug_active = forms.ChoiceField(choices=(('yes', 'Yes'), ('no', 'No')), widget=forms.RadioSelect)

    class Meta:
        model = PrescribedMedicine
        fields = '__all__'

    def clean(self):
        clean_data = self.cleaned_data
        if clean_data.get('start_date') > clean_data.get('stop_date'):
            raise ValidationError({'start_date': 'Start Date cannot be Greater then Policy End Date.'})
        if clean_data.get('dr_id') is None and clean_data.get('prescribing_doctor') is None:
            raise ValidationError("Doctor Name or Doctor id is needed.")
        return super(MedicineForm, self).clean()


class NotMedicineForm(forms.ModelForm):
    class Meta:
        model = UnPrescribeMedicine
        fields = '__all__'


class LabForm(forms.ModelForm):
    class Meta:
        model = Lab
        fields = '__all__'


class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = '__all__'


class ProcedureForm(forms.ModelForm):
    class Meta:
        model = VaccinationProcedure
        fields = '__all__'


class FamilyHistoryForm(forms.ModelForm):
    class Meta:
        model = FamilyHistory
        fields = '__all__'


class SocialHistoryForm(forms.ModelForm):
    smoking = forms.ChoiceField(choices=(('every_day', 'Current every day smoker'),
                                         ('some_day', 'Current some day smoker'),
                                         ('former_smoker', 'Former smoker'), ('never', 'Never smoker'),
                                         ('heavy_smoker', 'Heavy tobacco smoker'),
                                         ('light_smoker', 'Light tobacco smoker')), widget=forms.RadioSelect)
    alcohol = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')), widget=forms.RadioSelect)
    caffeine = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')), widget=forms.RadioSelect)
    drug = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')), widget=forms.RadioSelect)
    exercise = forms.ChoiceField(choices=(('yes', 'Yes'), ('no', 'No'), ('sometimes', 'Sometimes')),
                                 widget=forms.RadioSelect)

    class Meta:
        model = SocialHistory
        fields = '__all__'


class MedicalNoteForm(forms.ModelForm):
    visits = forms.ChoiceField(choices=(('int', 'Internal'), ('ext', 'External')), widget=forms.RadioSelect)

    class Meta:
        model = MedicalNotes
        fields = '__all__'


class MarForm(forms.ModelForm):
    class Meta:
        model = MarModel
        fields = '__all__'


class DrugDictionaryForm(forms.ModelForm):
    active = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')), widget=forms.RadioSelect)
    obsolete = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')), widget=forms.RadioSelect)

    class Meta:
        model = DrugDictionary
        fields = '__all__'


class VendorDictionaryForm(forms.ModelForm):
    active = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')), widget=forms.RadioSelect)

    class Meta:
        model = VendorDictionary
        fields = '__all__'


class MedicalProviderForm(forms.ModelForm):
    class Meta:
        model = MedicalProvider
        fields = "__all__"
