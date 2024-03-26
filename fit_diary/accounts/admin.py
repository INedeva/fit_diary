from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from fit_diary.accounts.forms import FitDiaryUserCreationForm, FitDiaryUserChangeForm

# Register your models here.


UserModel = get_user_model()


@admin.register(UserModel)
class FitDiaryUserAdmin(UserAdmin):
    model = UserModel
    add_form = FitDiaryUserCreationForm
    form = FitDiaryUserChangeForm

    list_display = ('pk', 'email', 'is_staff', 'is_active', 'is_superuser', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('email',)
    ordering = ('pk',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )
