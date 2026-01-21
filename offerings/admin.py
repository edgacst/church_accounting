
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.humanize.templatetags.humanize import intcomma
from .models import OfferingType, Offering, TaxCertificateIssueLog

@admin.register(OfferingType)
class OfferingTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']

@admin.register(Offering)
class OfferingAdmin(admin.ModelAdmin):

    def amount_with_comma(self, obj):
        return format_html('<div style="text-align:right; min-width:80px;">{}원</div>', intcomma(obj.amount))
    amount_with_comma.short_description = '금액'
    amount_with_comma.admin_order_field = 'amount'

    list_display = ['offering_date', 'member', 'offering_type', 
                   'amount_with_comma', 'payment_method', 'is_confirmed']
    list_filter = ['offering_date', 'offering_type', 'payment_method', 'is_confirmed']
    search_fields = ['member__korean_name', 'member__member_id', 'reference_number']
    date_hierarchy = 'offering_date'
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 50
    
    fieldsets = (
        ('헌금 정보', {
            'fields': ('member', 'offering_type', 'amount', 
                      'offering_date', 'worship_date')
        }),
        ('결제 정보', {
            'fields': ('payment_method', 'bank_name', 
                      'account_number', 'reference_number')
        }),
        ('관리 정보', {
            'fields': ('is_confirmed', 'notes')
        }),
        ('시스템 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TaxCertificateIssueLog)
class TaxCertificateIssueLogAdmin(admin.ModelAdmin):
    list_display = ['issued_at', 'member', 'year', 'issue_type', 'issued_by']
    list_filter = ['issue_type', 'year', 'issued_at']
    search_fields = ['member__korean_name', 'member__member_id']
    date_hierarchy = 'issued_at'
    readonly_fields = ['issued_at']
    list_per_page = 50