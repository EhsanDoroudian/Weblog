from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import CustomUserModel
from accounts.forms import  CustomUserCreateForm, CustomUserChangeForm 



class CustomUserAdmin(UserAdmin):
    model = CustomUserModel
    form = CustomUserChangeForm
    fieldsets = UserAdmin.fieldsets+(
        (
            None, {'fields': ('age', 'gender')}
        ),
    )
    add_form = CustomUserCreateForm
    add_fieldsets = UserAdmin.fieldsets+(
        (
            None, {'fields': ('age', 'gender')}
        ),
    )
    list_display = [
        "email",
        "username",
        "is_staff",
        "is_active",
    ]


admin.site.register(CustomUserModel, CustomUserAdmin)
