from django.contrib import admin
from .models import User, StudentProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'username',
        'email',
        'role',
        'is_active'
    )

    list_filter = (
        'role',
        'is_active'
    )

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'roll_no',
        'department',
        'kyc_status',
    )

    list_filter = (
        'department',
        'kyc_status',
    )

    search_fields = (
        'user__username',
        'roll_no',
        'department',
    )