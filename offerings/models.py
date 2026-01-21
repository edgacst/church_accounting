from django.db import models
from members.models import ChurchMember
from django.contrib.auth.models import User

class OfferingType(models.Model):
    """헌금 유형 (십일조, 감사헌금 등)"""
    name = models.CharField('헌금유형', max_length=50)
    code = models.CharField('코드', max_length=10, unique=True)
    description = models.TextField('설명', blank=True)
    is_active = models.BooleanField('활성화', default=True)
    
    class Meta:
        verbose_name = '헌금유형'
        verbose_name_plural = '헌금유형 관리'
    
    def __str__(self):
        return self.name

class Offering(models.Model):
    """헌금 기록"""
    PAYMENT_METHODS = [
        ('cash', '현금'),
        ('transfer', '계좌이체'),
        ('card', '카드'),
        ('check', '수표'),
    ]
    
    member = models.ForeignKey(ChurchMember, on_delete=models.CASCADE, 
                              verbose_name='헌금자', related_name='offerings')
    offering_type = models.ForeignKey(OfferingType, on_delete=models.PROTECT, 
                                     verbose_name='헌금유형')
    
    # 금액 정보
    amount = models.DecimalField('금액', max_digits=12, decimal_places=0)
    offering_date = models.DateField('헌금일자')
    worship_date = models.DateField('예배일자', null=True, blank=True)
    
    # 결제 정보
    payment_method = models.CharField('결제방법', max_length=20, 
                                     choices=PAYMENT_METHODS, default='cash')
    bank_name = models.CharField('은행명', max_length=50, blank=True)
    account_number = models.CharField('계좌번호', max_length=50, blank=True)
    reference_number = models.CharField('참조번호', max_length=100, blank=True)
    
    # 관리 정보
    is_confirmed = models.BooleanField('확인여부', default=False)
    notes = models.TextField('비고', blank=True)
    created_at = models.DateTimeField('등록일시', auto_now_add=True)
    updated_at = models.DateTimeField('수정일시', auto_now=True)
    
    class Meta:
        verbose_name = '헌금'
        verbose_name_plural = '헌금 관리'
        ordering = ['-offering_date', '-id']
    
    def __str__(self):
        return f"{self.member.korean_name} - {self.offering_type.name} - {self.amount:,}원"


class TaxCertificateIssueLog(models.Model):
    """증명서 발급 로그"""
    member = models.ForeignKey(ChurchMember, on_delete=models.CASCADE, verbose_name='교인', related_name='certificate_logs')
    year = models.IntegerField('증명서 연도')
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='발급자')
    issued_at = models.DateTimeField('발급일시', auto_now_add=True)
    issue_type = models.CharField('발급유형', max_length=20, choices=[
        ('html', 'HTML 조회'),
        ('pdf', 'PDF 다운로드'),
        ('print', '인쇄'),
    ], default='html')
    
    class Meta:
        verbose_name = '증명서 발급 로그'
        verbose_name_plural = '증명서 발급 로그'
        ordering = ['-issued_at']
    
    def __str__(self):
        return f"{self.member.korean_name} - {self.year}년 ({self.get_issue_type_display()})"