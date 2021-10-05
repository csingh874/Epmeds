from django.urls import path
from . import views
from .models import *

app_name = 'patients'
urlpatterns = [
    path('member-dashboard/', views.user_dashboard, name='member_dashboard'),
    path('add-member', views.add_member, name='add_member'),
    path('edit-member/<idx>', views.add_member, name="edit_member"),
    path('member-log/', views.member_log, name='member_log'),
    path('demographics-second/<idx>', views.demographics_second, name='demographics_sec'),
    path('advance-directive/<idx>', views.advance_directive, name='advance_directive'),
    path('emergency-contact/<idx>', views.emergency_contact, name='emergency_contact'),
    path('emergency-contact-delete', views.delete_record, {"model": EmergencyContact}, name='delete_emergency_contact'),
    path('medical-provider/<idx>', views.medical_provider, name="medical_provider"),
    path('insurance/<idx>', views.insurance, name="insurance_policy"),
    path('insurance-delete', views.delete_record, {"model": Insurance}, name="delete_insurance"),
    path('allergy/<idx>', views.allergy, name="allergy"),
    path('allergy-delete', views.delete_record, {"model": Allergies}, name="delete_allergy"),
    path('medication-prescribed/<idx>', views.medication_prescribed, name="medication_prescribed"),
    path('delete-prescribe-med', views.delete_record, {"model": PrescribedMedicine}, name='delete_prescribe_med'),
    path('not-to-prescribe-medication/<idx>', views.un_medication_prescribed, name="not_to_prescribe_medication"),
    path('delete-not-prescribe-med', views.delete_record, {"model": UnPrescribeMedicine}, name='delete_not_prescribe_med'),
    path('laboratory/<idx>', views.lab, name='lab'),
    path('delete-lab', views.delete_record, {"model": Lab}, name='delete_lab'),
    path('diagnosis/<idx>', views.diagnosis, name='diagnosis'),
    path('delete-diagnosis', views.delete_record, {"model": Diagnosis}, name='delete_diagnosis'),
    path('vaccination-procedure/<idx>', views.vaccination_procedure, name='vaccination_procedure'),
    path('delete-procedure', views.delete_record, {"model": VaccinationProcedure}, name='delete_procedure'),
    path('family-history/<idx>', views.family_history, name='family_history'),
    path('delete-family-history', views.delete_record, {"model": FamilyHistory}, name='delete_family_history'),
    path('social-history/<idx>', views.social_history, name='social_history'),
    path('medical-note/<idx>', views.medical_notes, name='medical_note'),
    path('delete-medical-note', views.delete_record, {"model": MedicalNotes}, name='delete_medical_note'),
    path('mar/<idx>', views.mar, name='mar'),
    path('delete-mar', views.delete_record, {"model": MarModel}, name='delete_mar'),
    path('delete-provider', views.delete_record, {"model": MedicalProvider}, name='delete_provider'),
    path('drug-dictionary/<idx>', views.drug_dictionary, name='drug_dictionary'),
    path('vendor-dictionary/<idx>', views.vendor_dictionary, name='vendor_dictionary'),
    path('send-data', views.get_user_data, name='get_user_data'),
    path('communication-log/<idx>', views.communication_log, name='communication_log'),
    path('chat/<idx>/<id>', views.chat, name='chat'),
]

