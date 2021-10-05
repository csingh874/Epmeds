from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.


@admin.register(CustomUser)
class CustomUserForm(UserAdmin):
    model = CustomUser

    list_display = ("id", "username",)
    readonly_fields = ("date_joined", "last_login")
    fieldsets = ((None, {'fields': ('username', 'password',)}),
                 ('Personal info', {'fields': ('account', 'first_name', 'last_name', 'middle_initiative', 'email', 'speciality', 'address', 'city',
                                               'state', 'zip_code', 'country', 'telephone', 'rec_date')}),
                 ('Doctor', {'fields': ('dr_grp', 'address2', 'city2', 'state2', 'zip_code2')}),
                 ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                 ('Important dates', {'fields': ('last_login', 'date_joined')}),
                 )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
