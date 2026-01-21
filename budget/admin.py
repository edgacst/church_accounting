from django.contrib import admin
from django.utils.html import format_html
from .models import AnnualBudget, BudgetTransaction


@admin.register(AnnualBudget)
class AnnualBudgetAdmin(admin.ModelAdmin):
    list_display = ('year',)  # 최소 필드만 남기고 테스트
    # list_display = ('year', 'department_name', 'total_amount', 'is_approved', 'created_at')
    list_filter = ('year', 'is_approved')
    search_fields = ('department_name',)
    ordering = ('-year', 'department_name')
    # list_editable = ('is_approved',)  # 목록에서 바로 승인 여부 수정 가능

@admin.register(BudgetTransaction)
class BudgetTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_date', 'description', 'amount', 'requester', 'status', 'receipt_preview')
    list_filter = ('status', 'transaction_date', 'budget__department_name')
    search_fields = ('description', 'requester__username', 'vendor')
    date_hierarchy = 'transaction_date'
    readonly_fields = ('created_at', 'updated_at', 'approved_at', 'approved_by')
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('budget', 'requester', 'transaction_date', 'amount')
        }),
        ('지출 상세', {
            'fields': ('description', 'vendor', 'notes', 'receipt')
        }),
        ('결재 상태', {
            'fields': ('status', 'approved_by', 'approved_at')
        }),
        ('시스템 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def receipt_preview(self, obj):
        if obj.receipt:
            return format_html('<a href="{}" target="_blank">보기</a>', obj.receipt.url)
        return "-"
    receipt_preview.short_description = "영수증"

    def save_model(self, request, obj, form, change):
        if not obj.requester:
            obj.requester = request.user
        super().save_model(request, obj, form, change)