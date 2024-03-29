from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from fit_diary.accounts.forms import FitDiaryUserCreationForm, FitDiaryUserChangeForm
from fit_diary.accounts.models import Profile

# Register your models here.


UserModel = get_user_model()


class ProfileInline(admin.StackedInline):
    # Viewing the user and its profile together in one place in the admin panel
    model = Profile
    can_delete = False  # The profile cannot be deleted without user deletion
    verbose_name = 'Profile'
    fk_name = 'user'


@admin.register(UserModel)
class FitDiaryUserAdmin(UserAdmin):
    model = UserModel
    add_form = FitDiaryUserCreationForm
    form = FitDiaryUserChangeForm
    inlines = (ProfileInline,)

    list_display = ('pk', 'email', 'is_staff', 'is_active', 'is_superuser', 'date_joined')
    list_display_links = ('pk', 'email',)
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('email',)
    ordering = ('pk',)
    list_per_page = 15

    fieldsets = (
        ('AUTH', {'fields': ('email', 'password')}),
        ('PERMISSIONS', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('DATES', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        ('AUTH', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )
