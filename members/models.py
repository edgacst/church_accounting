from django.db import models
from django.contrib.auth.models import User

class ChurchMember(models.Model):
    def delete(self, *args, **kwargs):
        # 연결된 User도 함께 삭제
        if self.user:
            self.user.delete()
        super().delete(*args, **kwargs)
    MEMBER_STATUS = [
        ('active', '등록교인'),
        ('inactive', '비활성'),
        ('visitor', '새신자'),
    ]
    
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]
    
    # User 계정과 1:1 연결
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='계정')
    # 기본 정보
    member_id = models.CharField('교인번호', max_length=20, unique=True, blank=True)
    korean_name = models.CharField('한글이름', max_length=50)
    english_name = models.CharField('영문이름', max_length=50, blank=True)
    gender = models.CharField('성별', max_length=1, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField('생년월일', null=True, blank=True)
    baptism_date = models.DateField('세례일', null=True, blank=True)
    
    # 가족 관계
    family_id = models.CharField('가족번호', max_length=20, blank=True)
    relationship = models.CharField('가족관계', max_length=20, blank=True)
    
    # 연락처
    phone = models.CharField('휴대전화', max_length=20)
    email = models.EmailField('이메일', blank=True)
    address = models.TextField('주소', blank=True)
    
    # 교회 정보
    department = models.CharField('부서', max_length=50, blank=True)
    position = models.CharField('직분', max_length=50, blank=True)
    status = models.CharField('상태', max_length=20, choices=MEMBER_STATUS, default='active')
    
    # 헌금 관련
    offering_number = models.CharField('헌금봉투번호', max_length=20, unique=True, null=True, blank=True)
    tax_issuance_consent = models.BooleanField('세금공제동의', default=False)
    
    # 관리 정보
    created_at = models.DateTimeField('등록일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)
    notes = models.TextField('비고', blank=True)
    
    class Meta:
        verbose_name = '교인'
        verbose_name_plural = '교인 관리'
        ordering = ['korean_name']
    
    def save(self, *args, **kwargs):
        # member_id가 없거나, 이미 존재하는 값이면 새로 생성 (6자리 숫자 일련번호)
        if not self.member_id or ChurchMember.objects.filter(member_id=self.member_id).exclude(pk=self.pk).exists():
            # 가장 큰 숫자형 member_id를 찾아서 +1
            last = ChurchMember.objects.exclude(member_id=None).exclude(member_id='').order_by('-member_id').first()
            if last and last.member_id.isdigit():
                new_id = str(int(last.member_id) + 1).zfill(6)
            else:
                new_id = '000001'
            while ChurchMember.objects.filter(member_id=new_id).exists():
                new_id = str(int(new_id) + 1).zfill(6)
            self.member_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.korean_name} ({self.member_id})"