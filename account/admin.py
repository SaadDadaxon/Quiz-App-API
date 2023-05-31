from django.contrib import admin
from .forms import AccountChangeForms, AccountCreateForms
from .models import Account
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    form = AccountChangeForms
    add_form = AccountCreateForms
    add_fieldsets = (
        (None, {'classes': ('wide', ), "fields": ('email', 'password', 'password2'), }),
    )
    list_display = ('id', 'email', 'full_name', 'image_tag', 'is_superuser', 'is_active', 'is_staff', 'create_date')
    readonly_fields = ('create_date', )
    list_filter = ('is_superuser', 'is_active', 'is_staff')
    fieldsets = (
        (None, {"fields": ('email', 'password', 'full_name', 'image'), }),
        ("Permission", {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions'), }),
        ("Important dates", {'fields': ('create_date', ), }),
    )
    ordering = None
    search_fields = ('email', 'full_name')


admin.site.register(Account, AccountAdmin)
