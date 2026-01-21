from django.db import models
from django.conf import settings
from django.db.models import Sum

class AnnualBudget(models.Model):
    """연간 예산 모델"""
    year = models.IntegerField(verbose_name="연도")
    department_name = models.CharField(max_length=100, verbose_name="부서명")
    total_amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="예산 총액")
    is_approved = models.BooleanField(default=False, verbose_name="승인 여부")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.year}년 {self.department_name} 예산"

    class Meta:
        verbose_name = "연간 예산"
        verbose_name_plural = "연간 예산 목록"

    @property
    def spent_amount(self):
        """승인된 지출 총액"""
        approved_transactions = self.transactions.filter(status='approved')
        return approved_transactions.aggregate(total=Sum('amount'))['total'] or 0

    @property
    def balance(self):
        """잔액 (총 예산 - 승인된 지출)"""
        return self.total_amount - self.spent_amount

class BudgetTransaction(models.Model):
    """지출 내역 및 신청 모델"""
    STATUS_CHOICES = [
        ('pending', '승인 대기'),
        ('approved', '승인됨'),
        ('rejected', '반려됨'),
    ]

    budget = models.ForeignKey(AnnualBudget, on_delete=models.CASCADE, related_name='transactions', verbose_name="관련 예산")
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="신청자")
    transaction_date = models.DateField(verbose_name="지출 일자")
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="금액")
    description = models.TextField(verbose_name="지출 내용")
    vendor = models.CharField(max_length=100, verbose_name="거래처", blank=True)
    notes = models.TextField(verbose_name="비고", blank=True)
    receipt = models.ImageField(upload_to='receipts/%Y/%m/', blank=True, null=True, verbose_name="영수증")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="결재 상태")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_transactions', verbose_name="결재자")
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name="결재 일시")
    rejection_reason = models.TextField(verbose_name="반려 사유", blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_date} - {self.description} ({self.amount}원)"

    class Meta:
        verbose_name = "지출 내역"
        verbose_name_plural = "지출 내역 목록"


class CashTransaction(models.Model):
    """현금 입출금 내역 (현금출납부)"""
    TRANSACTION_TYPES = [
        ('income', '수입'),
        ('expense', '지출'),
    ]
    
    transaction_date = models.DateField('거래일자')
    transaction_type = models.CharField('구분', max_length=10, choices=TRANSACTION_TYPES)
    description = models.CharField('적요', max_length=200)
    amount = models.DecimalField('금액', max_digits=12, decimal_places=0)
    
    # 관련 정보
    category = models.CharField('분류', max_length=50, blank=True, help_text='예: 헌금, 사례비, 시설비 등')
    payer_receiver = models.CharField('수입/지출처', max_length=100, blank=True)
    notes = models.TextField('비고', blank=True)
    
    # 관리 정보
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='등록자')
    created_at = models.DateTimeField('등록일시', auto_now_add=True)
    updated_at = models.DateTimeField('수정일시', auto_now=True)
    
    class Meta:
        verbose_name = '현금거래'
        verbose_name_plural = '현금출납부'
        ordering = ['transaction_date', 'id']
    
    def __str__(self):
        return f"{self.transaction_date} - {self.get_transaction_type_display()} - {self.description}"
