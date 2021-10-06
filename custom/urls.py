from django.urls import path, re_path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'custom'
urlpatterns = [
    # path('', views.home_view),
    # path('services/', views.services_view),
    # path('what_we_do/', views.what_we_do),
    # path('become_member/', views.become_member),
    # path('career/', views.career),
    # path('contact_us/', views.contact_us),
    # path('logout/', views.user_logout, name='user_logout'),
    # re_path(r'^signup/(provider|member)$', views.register_mem_prov, name="user_signup"),
    # re_path(r'^login/(provider|member)$', views.user_login, name='user_login'),
    # path('forgot_password/', views.forgot_password, name='forgot_password'),
    # path('change-password/<idx>', views.verify_otp, name='verify_otp'),
]
