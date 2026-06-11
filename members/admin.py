from django.contrib import admin
from django.utils.html import format_html
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'kyc_status',
        'view_document'
    )

    def view_document(self, obj):

        if obj.id_proof:

            return format_html(
                '<a href="{}" target="_blank">View KYC</a>',
                obj.id_proof.url
            )

        return "No Document"