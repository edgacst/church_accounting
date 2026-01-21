# budget/cashbook_models.py
"""
현금출납부 관련 모델
나중에 models.py에 통합할 예정
"""
from django.db import models
from django.conf import settings
from django.utils import timezone

class CashTransaction(models.Model):
    """현금 입출금 내역"""
    TRANSACTION_TYPES = [
        ('income', '수입'),
        ('expense', '지출'),
    ]
    
    transaction_date = models.DateField('거래일자', default=timezone.now)
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
    
    # 잔액 계산을 위한 필드
    balance = models.DecimalField('잔액', max_digits=12, decimal_places=0, default=0)
    
    class Meta:
        verbose_name = '현금거래'
        verbose_name_plural = '현금출납부'
        ordering = ['transaction_date', 'id']
    
    def __str__(self):
        return f"{self.transaction_date} - {self.get_transaction_type_display()} - {self.description}"
    
    def save(self, *args, **kwargs):
        # 잔액 자동 계산
        super().save(*args, **kwargs)
        self.update_balances()
    
    @classmethod
    def update_balances(cls):
        """모든 거래의 잔액을 순차적으로 업데이트"""
        transactions = cls.objects.all().order_by('transaction_date', 'id')
        balance = 0
        
        for transaction in transactions:
            if transaction.transaction_type == 'income':
                balance += transaction.amount
            else:
                balance -= transaction.amount
            
            # 직접 업데이트 (save() 재호출 방지)
            cls.objects.filter(pk=transaction.pk).update(balance=balance)
