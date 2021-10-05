from django.urls import path
from . import views

app_name = 'doctors'
urlpatterns = [
    path('doctor_dictionary/', views.doctor_dictionary, name='doctor_dictionary'),
    path('patient-portal/', views.patient_portal, name='patient_portal'),
    path('search_user/', views.search_user),
    path('communication_log/', views.communication_log),
    path('user-logout', views.user_logout, name='user_logout'),
    path('get-patient-data', views.get_patient_data, name='get_patient_data'),
    path('chat/<idx>', views.chat_view, name='chat'),
]
