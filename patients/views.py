from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth import get_user_model
from doctors.models import CommunicationLog
# Create your views here.


def get_data(model_name, **kwargs):
    try:
        return model_name.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None


def write_logs(**kwargs):
    MemberLogs.objects.create(**kwargs)


@login_required(login_url='/login_page')
def user_dashboard(request):
    patient_data = Member.objects.values('first_name', 'last_name', 'dob', 'sex', 'idx')
    context = {"patient_data": patient_data}
    return render(request, 'member/user_dashboard.html', context)


@login_required(login_url='/login_page')
def add_member(request, idx=None):
    member = get_data(Member, idx=idx)
    form = AddPatient() if member is None else AddPatient(instance=member)
    if member:
        write_logs(access_by=member, action='View', data_access='Demographics Data View')
    if request.method == 'POST':
        form = AddPatient(request.POST) if member is None else AddPatient(instance=member, data=request.POST)
        if form.is_valid():
            partial_form = form.save(commit=False)
            partial_form.parent_user = request.user
            partial_form.save()
            if not member:
                write_logs(access_by=member, action='Add', data_access='Added Demographics Data')
            else:
                write_logs(access_by=member, action='Update', data_access='Updated Demographics Data')
            return redirect(reverse('patients:edit_member', kwargs={'idx': partial_form.idx}))
    return render(request, 'member/add_member.html', {'form': form, 'idx': idx})


@login_required(login_url='/login_page')
def member_log(request):
    data = MemberLogs.objects.all()
    return render(request, 'member/member_log.html', {'data': data})


@login_required(login_url='/login_page')
def demographics_second(request, idx):
    member = get_object_or_404(Member, idx=idx)
    emp = get_data(EmploymentInfo, member_id=member)
    form = EmploymentInfoForm() if emp is None else EmploymentInfoForm(instance=emp)
    write_logs(access_by=member, action='View', data_access='Employment Data View')
    if request.method == 'POST':
        form = EmploymentInfoForm(request.POST) if emp is None else EmploymentInfoForm(instance=emp, data=request.POST)
        if form.is_valid():
            partial_form = form.save(commit=False)
            partial_form.member_id = member
            partial_form.save()
            if emp:
                write_logs(access_by=member, action='Update', data_access='Updated Employment Data View')
            else:
                write_logs(access_by=member, action='Add', data_access='Added Employment Data')
            return redirect(reverse('patients:demographics_sec', kwargs={'idx': idx}))
    return render(request, 'member/demographics_second.html', {'form': form, 'idx': idx})


@login_required(login_url='/login_page')
def advance_directive(request, idx):
    member = get_object_or_404(Member, idx=idx)
    adv = get_data(AdvanceDirectives, member_id=member)
    form = AdvanceDirectiveForm() if adv is None else AdvanceDirectiveForm(instance=adv)
    write_logs(access_by=member, action='View', data_access='Advance Directive View')
    if request.method == 'POST':
        form = AdvanceDirectiveForm(request.POST, request.FILES) if adv is None else \
            AdvanceDirectiveForm(instance=adv, data=request.POST)
        if form.is_valid():
            partial_form = form.save(commit=False)
            partial_form.member_id = member
            partial_form.save()
            if adv:
                write_logs(access_by=member, action='Update', data_access='Updated Advance Directive Data View')
            else:
                write_logs(access_by=member, action='Add', data_access='Added Advance Directive Data')
            return redirect(reverse('patients:advance_directive', kwargs={'idx': idx}))
    return render(request, 'member/advance_directives.html', {'form': form, 'idx': idx})


@login_required(login_url='/login_page')
def emergency_contact(request, idx):
    member = get_object_or_404(Member, idx=idx)
    employee_data = EmergencyContact.objects.filter(member_id=member)
    write_logs(access_by=member, action='View', data_access='Emergency Contact Details View')
    form = EmergencyContactForm()
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            partial_form = form.save(commit=False)
            partial_form.member_id = member
            partial_form.save()
            write_logs(access_by=member, action='Add', data_access='Added Emergency Contact Details')
            return redirect(reverse('patients:emergency_contact', kwargs={'idx': idx}))
    return render(request, 'member/emergency_contact.html', {'form': form, 'idx': idx, 'data': employee_data})


@login_required(login_url='/login_page')
def delete_record(request, model):
    if request.method == 'POST':
        user_idx = request.POST.get('user_idx')
        adv = get_data(model, id=user_idx)
        adv.delete()
        return JsonResponse({'success': 'Record Deleted Successfully'})


def medical_provider(request, idx):
    member = get_object_or_404(Member, idx=idx)
    provider_data = MedicalProvider.objects.filter(member_id=member)
    form = MedicalProviderForm()
    write_logs(access_by=member, action='View', data_access='Medical Provider View')
    if request.method == 'POST':
        form = MedicalProviderForm(request.POST)
        if form.is_valid():
            partial_form = form.save(commit=False)
            partial_form.member_id = member
            partial_form.save()
            write_logs(access_by=member, action='Add', data_access='Medical Provider Data Added')
            return redirect(reverse('patients:medical_provider', kwargs={'idx': idx}))
    return render(request, 'member/medical_provider.html', {'idx': idx, 'form': form, 'provider_data': provider_data})


@login_required(login_url='/login_page')
def insurance(request, idx):
    member = get_object_or_404(Member, idx=idx)
    policy_data = Insurance.objects.filter(member=member)
    form = InsuranceForm()
    write_logs(access_by=member, action='View', data_access='Insurance Data View')
    if request.method == 'POST':
        form = InsuranceForm(request.POST)
        if form.is_valid():
            policy_holder_id = str(form.cleaned_data['policy_holder']).split(" ")[0]
            form.cleaned_data['policy_holder'] = policy_holder_id
            partial_form = form.save(commit=False)
            partial_form.member = member
            partial_form.save()
            write_logs(access_by=member, action='Add', data_access='Insurance Data Added')
            return redirect(reverse('patients:insurance_policy', kwargs={'idx': idx}))
    return render(request, 'member/insurance.html', {'idx': idx, 'form': form, 'policy_data': policy_data})


@login_required(login_url='/login_page')
def allergy(request, idx):
    member = get_object_or_404(Member, idx=idx)
    allergy_data = Allergies.objects.filter(member_id=member)
    write_logs(access_by=member, action='View', data_access='Allergies Data View')
    form = AllergyForm()
    if request.method == 'POST':
        form = AllergyForm(request.POST)
        if form.is_valid():
            partial_form = form.save(commit=False)
            partial_form.member_id = member
            partial_form.save()
            write_logs(access_by=member, action='Add', data_access='Allergies Data Added')
            return redirect(reverse('patients:allergy', kwargs={'idx': idx}))
    return render(request, 'member/allergy.html', {'form': form, 'idx': idx, 'allergy_data': allergy_data})


@login_required(login_url='/login_page')
def medication_prescribed(request, idx):
    member = get_object_or_404(Member, idx=idx)
    medicine_data = PrescribedMedicine.objects.filter(member_id=member)
    form = MedicineForm()
    write_logs(access_by=member, action='View', data_access='Medication Prescribed Data View')
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            dr_id = form.cleaned_data.get('dr_id')
            partial_form = form.save(commit=False)
            partial_form.member_id = member
            partial_form.dr_id = dr_id
            partial_form.save()
            write_logs(access_by=member, action='Add', data_access='Medication Prescribed Data Added')
            return redirect(reverse('patients:medication_prescribed', kwargs={'idx': idx}))
    return render(request, 'member/medications_prescribed.html', {'form': form, 'idx': idx, 'medicine_data': medicine_data})


@login_required(login_url='/login_page')
def un_medication_prescribed(request, idx):
    member = get_object_or_404(Member, idx=idx)
    medicine_data = UnPrescribeMedicine.objects.filter(member_id=member)
    form = NotMedicineForm()
    write_logs(access_by=member, action='View', data_access='Medication Not to Prescribed Data View')
    if request.method == 'POST':
        form = NotMedicineForm(request.POST)
        if form.is_valid():
            partial_form = form.save(commit=False)
            partial_form.member_id = member
            partial_form.save()
            write_logs(access_by=member, action='Add', data_access='Medication Not to Prescribed Data Added')
            return redirect(reverse('patients:not_to_prescribe_medication', kwargs={'idx': idx}))
    return render(request, 'member/medicationnotpros.html', {'form': form, 'idx': idx, 'medicine_data': medicine_data})


@login_required(login_url='/login_page')
def lab(request, idx):
    member = get_object_or_404(Member, idx=idx)
    lab_data = Lab.objects.filter(member_id=member)
    form = LabForm()
    write_logs(access_by=member, action='View', data_access='Lab Data View')
    if request.method == 'POST':
        form = LabForm(request.POST)
        if form.is_valid():
            partial_form = form.save(commit=False)
            partial_form.member_id = member
            partial_form.save()
            write_logs(access_by=member, action='Add', data_access='Lab Data Added')
            return redirect(reverse('patients:lab', kwargs={'idx': idx}))
    return render(request, 'member/lab.html', {'form': form, 'idx': idx, 'lab_data': lab_data})


@login_required(login_url='/login_page')
def diagnosis(request, idx):
    member = get_object_or_404(Member, idx=idx)
    diagnosis_data = Diagnosis.objects.filter(member_id=member)
    form = DiagnosisForm()
    write_logs(access_by=member, action='View', data_access='Diagnosis Data View')
    if request.method == 'POST':
        form = DiagnosisForm(request.POST)
        if form.is_valid():
            partial_form = form.save(commit=False)
            partial_form.member_id = member
            partial_form.save()
            write_logs(access_by=member, action='Add', data_access='Diagnosis Data Added')
            return redirect(reverse('patients:diagnosis', kwargs={'idx': idx}))
    return render(request, 'member/diagnosis.html', {'form': form, 'idx': idx, 'diagnosis_data': diagnosis_data})


@login_required(login_url='/login_page')
def vaccination_procedure(request, idx):
    member = get_object_or_404(Member, idx=idx)
    procedure_data = VaccinationProcedure.objects.filter(member_id=member)
    form = ProcedureForm()
    write_logs(access_by=member, action='View', data_access='Vaccination Procedure Data View')
    if request.method == 'POST':
        form = ProcedureForm(request.POST)
        if form.is_valid():
            partial_form = form.save(commit=False)
            partial_form.member_id = member
            partial_form.save()
            write_logs(access_by=member, action='Add', data_access='Vaccination Procedure Data Added')
            return redirect(reverse('patients:vaccination_procedure', kwargs={'idx': idx}))
    return render(request, 'member/vaccination.html', {'form': form, 'idx': idx, 'procedure_data': procedure_data})


@login_required(login_url='/login_page')
def family_history(request, idx):
    member = get_object_or_404(Member, idx=idx)
    family_data = FamilyHistory.objects.filter(member_id=member)
    write_logs(access_by=member, action='View', data_access='Family History Data View')
    form = FamilyHistoryForm()
    if request.method == 'POST':
        form = FamilyHistoryForm(request.POST)
        if form.is_valid():
            partial_form = form.save(commit=False)
            partial_form.member_id = member
            partial_form.save()
            write_logs(access_by=member, action='Add', data_access='Family History Data Added')
            return redirect(reverse('patients:family_history', kwargs={'idx': idx}))
    return render(request, 'member/family_history.html', {'form': form, 'idx': idx, 'family_data': family_data})


@login_required(login_url='/login_page')
def social_history(request, idx):
    member = get_object_or_404(Member, idx=idx)
    hist = get_data(SocialHistory, member_id=member)
    form = SocialHistoryForm() if hist is None else SocialHistoryForm(instance=hist)
    write_logs(access_by=member, action='View', data_access='Social History Data View')
    if request.method == 'POST':
        form = SocialHistoryForm(request.POST) if member is None else SocialHistoryForm(instance=hist, data=request.POST)
        if form.is_valid():
            partial_form = form.save(commit=False)
            partial_form.member_id = member
            partial_form.save()
            write_logs(access_by=member, action='Add', data_access='Social History Data Added')
            return redirect(reverse('patients:social_history', kwargs={'idx': idx}))
    return render(request, 'member/social_history.html', {'form': form, 'idx': idx})


@login_required(login_url='/login_page')
def medical_notes(request, idx):
    member = get_object_or_404(Member, idx=idx)
    medical_data = MedicalNotes.objects.filter(member_id=member)
    write_logs(access_by=member, action='View', data_access='Medical Notes Data View')
    form = MedicalNoteForm()
    if request.method == 'POST':
        form = MedicalNoteForm(request.POST)
        if form.is_valid():
            partial_form = form.save(commit=False)
            partial_form.member_id = member
            partial_form.save()
            write_logs(access_by=member, action='Add', data_access='Medical Notes Data Added')
            return redirect(reverse('patients:medical_note', kwargs={'idx': idx}))
    return render(request, 'member/medical_notes.html', {'form': form, 'idx': idx, 'medical_data': medical_data})


@login_required(login_url='/login_page')
def mar(request, idx):
    member = get_object_or_404(Member, idx=idx)
    mar_data = MarModel.objects.filter(member_id=member)
    write_logs(access_by=member, action='View', data_access='Mar Data Added')
    form = MarForm()
    if request.method == 'POST':
        form = MarForm(request.POST)
        if form.is_valid():
            partial_form = form.save(commit=False)
            partial_form.member_id = member
            partial_form.save()
            write_logs(access_by=member, action='Add', data_access='Mar Data Added')
            return redirect(reverse('patients:mar', kwargs={'idx': idx}))
    return render(request, 'member/mar.html', {'form': form, 'idx': idx, 'mar_data': mar_data})


@login_required(login_url='/login_page')
def drug_dictionary(request, idx):
    member = get_object_or_404(Member, idx=idx)
    drug_dict = get_data(DrugDictionary, member_id=member)
    form = DrugDictionaryForm() if drug_dict is None else DrugDictionaryForm(instance=drug_dict)
    write_logs(access_by=member, action='View', data_access='Drug Dictionary Data View')
    if request.method == 'POST':
        form = DrugDictionaryForm(instance=drug_dict, data=request.POST) if drug_dict else DrugDictionaryForm(request.POST)
        if form.is_valid():
            partial_form = form.save(commit=False)
            partial_form.member_id = member
            partial_form.save()
            if drug_dict:
                write_logs(access_by=member, action='Update', data_access='Drug Dictionary Data Updated')
            else:
                write_logs(access_by=member, action='Add', data_access='Drug Dictionary Data Added')
            return redirect(reverse('patients:drug_dictionary', kwargs={'idx': idx}))
    return render(request, 'member/drug_dictionary.html', {'form': form, 'idx': idx})


@login_required(login_url='/login_page')
def vendor_dictionary(request, idx):
    member = get_object_or_404(Member, idx=idx)
    drug_dict = get_data(VendorDictionary, member_id=member)
    write_logs(access_by=member, action='View', data_access='Vendor Dictionary Data View')
    form = VendorDictionaryForm() if drug_dict is None else VendorDictionaryForm(instance=drug_dict)
    if request.method == 'POST':
        form = VendorDictionaryForm(instance=drug_dict, data=request.POST) if drug_dict else VendorDictionaryForm(request.POST)
        if form.is_valid():
            partial_form = form.save(commit=False)
            partial_form.member_id = member
            partial_form.save()
            if drug_dict:
                write_logs(access_by=member, action='Update', data_access='Vendor Dictionary Data Updated')
            else:
                write_logs(access_by=member, action='Add', data_access='Vendor Dictionary Data Added')
            return redirect(reverse('patients:vendor_dictionary', kwargs={'idx': idx}))
    return render(request, 'member/vendor_dictionary.html', {'form': form, 'idx': idx})


@login_required(login_url='/login_page')
def communication_log(request, idx):
    msgs = get_user_model().objects.values('username', 'id', 'communicationlog__messages', 'communicationlog__create_date', 'communicationlog__status').\
        filter(groups__name='provider').order_by('id', '-communicationlog__id').distinct('id')
    return render(request, 'member/communication.html', {'idx': idx, 'msgs': msgs})


@login_required(login_url='/login_page')
def chat(request, idx, id):
    patient_id = get_object_or_404(Member, idx=idx)
    doctor_id = get_object_or_404(get_user_model(), id=id)
    messages = CommunicationLog.objects.filter(patient_id__idx=idx, doctor_id=doctor_id)
    chat_data = CommunicationLog.objects.filter(patient_id__idx=idx, doctor_id__id=id).order_by('-id')[0]
    chat_data.status = 'view'
    chat_data.save()
    if request.method == "POST":
        msg = request.POST.get('msg')
        if msg is not None:
            CommunicationLog.objects.create(messages=msg, sent_by='pat', doctor_id=doctor_id, patient_id=patient_id)
            return redirect(reverse('patients:chat', args=[idx, id]))
    return render(request, 'member/chat.html', {'idx': idx, "messages": messages})


def get_user_data(request):
    if request.method == 'GET':
        idx = request.GET.get('idx')
        data = get_object_or_404(get_user_model(), id=idx)
        obj = {'first_name': data.first_name, 'last_name': data.last_name, 'address': data.address,
                'zip_code': data.zip_code, 'telephone': data.telephone}
        return JsonResponse(obj)
