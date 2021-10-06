# from django.http import HttpResponse
# from django.shortcuts import redirect, render
# from django.urls import reverse
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from django.contrib.auth.models import Group
# from django.contrib.auth.decorators import login_required
# from .forms import CustomUserCreationForm
# import pyotp
# from django.core.mail import send_mail
# from asgiref.sync import sync_to_async
# import base64
# import asyncio
# from django.contrib.auth.forms import SetPasswordForm
# import uuid
# from django.conf import settings
# from django.contrib.auth import get_user_model
# # Create your views here.
#
#
# def home_view(request):
#     return render(request, 'home_page.html')
#
#
# def services_view(request):
#     return render(request, 'services.html')
#
#
# def what_we_do(request):
#     return render(request, 'what_we_do.html')
#
#
# def become_member(request):
#     return render(request, 'become_member.html')
#
#
# def career(request):
#     return render(request, 'career.html')
#
#
# def contact_us(request):
#     return render(request, 'contact_us.html')
#
#
# async def send_otp_mail(sub, msg, email):
#     a_send_mail = sync_to_async(send_mail)
#     await a_send_mail(sub, msg, settings.EMAIL_HOST_USER, email, fail_silently=False)
#
#
# def user_login(request, user_type):
#     if request.user.is_authenticated:
#         group = list(request.user.groups.values_list('name', flat=True))
#         if 'member' in group:
#             return redirect('patients:member_dashboard')
#         elif 'provider' in group:
#             return redirect('doctors:doctor_dictionary')
#     form = CustomUserCreationForm()
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             group = list(user.groups.values_list('name', flat=True))
#             if 'member' in group and 'member' == user_type:
#                 return redirect('patients:member_dashboard')
#             elif 'provider' in group and 'provider' == user_type:
#                 return redirect('doctors:doctor_dictionary')
#             else:
#                 messages.error(request, 'We believe you are trying to login through the wrong member portal', extra_tags='login')
#                 return redirect(reverse('custom:user_login', args=[user_type]))
#         messages.error(request, 'Username or Password is incorrect.', extra_tags='login')
#     return render(request, "base_login.html", {'user_type': user_type, 'form': form})
#
#
# def user_logout(request):
#     logout(request)
#     return redirect('/')
#
#
# def register_mem_prov(request, user_type):
#     if request.user.is_authenticated:
#         group = list(request.user.groups.values_list('name', flat=True))
#         if 'member' in group:
#             return redirect('patients:member_dashboard')
#         elif 'provider' in group:
#             return redirect('doctors:doctor_dictionary')
#     form = CustomUserCreationForm()
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             partial_form = form.save()
#             user_group = Group.objects.get(name=user_type)
#             partial_form.groups.add(user_group)
#             messages.success(request, "Account created successfully", extra_tags='signup')
#             return redirect(reverse('custom:user_login', args=[user_type]))
#     return render(request, 'base_login.html', {'form': form, 'user_type': user_type})
#
#
# async def forgot_password(request):
#     if request.method == "POST":
#         try:
#             user = await sync_to_async(get_user_model().objects.values('email').get)(email=request.POST.get('email'))
#             idx = uuid.uuid4()
#             key = base64.b32encode(bytes(str(idx), encoding='utf-8'))
#             totp = pyotp.TOTP(key, interval=300, name=user.get('email'))
#             sub = "Password reset otp."
#             msg = f"Hi\n Your otp is {totp.now()}."
#             asyncio.create_task(send_otp_mail(sub, msg, list(user.get('email'))))
#         except get_user_model().DoesNotExist:
#             messages.error(request, 'Email Id is not registered with us.')
#         return redirect(reverse('custom:verify_otp', args=[idx]))
#     return render(request, 'forgot_password.html')
#
#
# def verify_otp(request, idx):
#     if request.method == "POST":
#         try:
#             email = request.POST.get('email')
#             user = get_user_model().objects.get(email=email)
#         except get_user_model().DoesNotExist:
#             messages.error(request, 'Incorrect Email address')
#             return redirect(reverse('custom:verify_otp', args=[idx]))
#         otp_num = int(request.POST.get('otp'))
#         key = base64.b32encode(bytes(str(idx), encoding='utf-8'))
#         totp = pyotp.TOTP(key, interval=300, name=email)
#         if totp.verify(otp_num) is False:
#             messages.error(request, "Invalid otp number.")
#             return redirect(reverse('custom:verify_otp', args=[idx]))
#         data = {"new_password1": request.POST.get('new_password'), "new_password2": request.POST.get('confirm_password')}
#         form = SetPasswordForm(data=data, user=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Password reset successfully", extra_tags='password')
#             return redirect(reverse('custom:user_login', args=['provider']))
#         messages.error(request, form.errors)
#     return render(request, 'otp.html',)
