from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Department

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'department', 'is_manager', 'is_staff')
    list_filter = ('is_manager', 'department', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('department', 'is_manager')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department)