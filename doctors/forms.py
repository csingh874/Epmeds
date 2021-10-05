from django import forms
from django.contrib.auth import get_user_model


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'address', 'city', 'zip_code', 'state', 'country', 'telephone', 'email',
                  'rec_date', 'account', 'speciality', 'dr_grp', 'address2', 'city2', 'state2', 'zip_code2', 'rec_date',
                  'middle_initiative', 'telephone2')


class PatientForm(forms.Form):
    visited_date = forms.DateField(required=True)
    dob = forms.DateField(required=True)
    last_name = forms.CharField(required=True)
    first_name = forms.CharField(required=False)
    ssn = forms.CharField(required=True)
    sex = forms.ChoiceField(choices=((None, 'Select'), ('male', 'Male'), ('female', 'Female'), ('unknown', 'Other')), required=True)
    age = forms.IntegerField(required=True)
    email = forms.EmailField(required=False)
    emg_name = forms.CharField(required=True)
    emg_email = forms.EmailField(required=True)
    emg_auth_rep = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')), widget=forms.RadioSelect)
    code_type = forms.ChoiceField(choices=(('icd10', 'ICD10'), ('icd9', 'ICD9')))
    diagnosis_code = forms.CharField()
    diagnosis_description = forms.CharField()
