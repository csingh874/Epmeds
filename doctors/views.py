from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .forms import *
from patients.models import EmergencyContact, Member
from .models import *
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth import get_user_model


# Create your views here.
@login_required(login_url='/login_page')
def doctor_dictionary(request):
    form = UserForm(instance=request.user)
    if request.method == 'POST':
        form = UserForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctors:doctor_dictionary')
    return render(request, 'provider/doctor_dictionary.html', {'form': form})


@login_required(login_url='/login_page')
def patient_portal(request):
    form = PatientForm()
    patient_data = Member.objects.values('idx', 'first_name', 'last_name', 'dob', 'ssn', 'sex', 'email')
    return render(request, 'provider/patient_portal.html', {'form': form, 'patient_data': patient_data})


@login_required(login_url='/login_page')
def search_user(request):
    return render(request, 'provider/search_user.html')


@login_required(login_url='/login_page')
def communication_log(request):
    msgs = Member.objects.values('first_name',  'last_name', 'idx', 'communicationlog__messages', 'communicationlog__create_date', 'communicationlog__status').\
        order_by('-id', '-communicationlog__id').distinct('id')
    return render(request, 'provider/communication_log.html', {'msgs': msgs})


def user_logout(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login_page')
def chat_view(request, idx):
    patient_id = get_object_or_404(Member, idx=idx)
    messages = CommunicationLog.objects.filter(patient_id__idx=idx, doctor_id=request.user.id)
    chat = CommunicationLog.objects.filter(patient_id__idx=idx).order_by('-id')[0]
    chat.status = 'view'
    chat.save()
    if request.method == "POST":
        msg = request.POST.get('msg')
        if msg is not None:
            CommunicationLog.objects.create(messages=msg, sent_by='dr', doctor_id=request.user, patient_id=patient_id)
            return redirect(reverse('doctors:chat', args=[idx]))
    return render(request, 'provider/chat.html', {"messages": messages})


@login_required(login_url='/login_page')
def get_patient_data(request):
    if request.method == "POST":
        idx = request.POST.get('user_idx')
        emp = EmergencyContact.objects.values("auth_rep", "first_name", "last_name", "email").filter(member_id__idx=idx)
        emp = {'first_name': "", "last_name": ""} if not emp else emp[0]
        return JsonResponse({'success': emp})
