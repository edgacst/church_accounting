import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'church_finance.settings')
django.setup()

from members.models import ChurchMember
from offerings.models import Offering
from django.contrib.auth.models import User

# 현재 사용자 확인
try:
    user = User.objects.get(username='ᄂ미0421')
    print(f'사용자: {user.username}')
    print(f'이메일: {user.email}')
    
    # 교인 정보 찾기
    print('\n=== 교인 찾기 ===')
    member = ChurchMember.objects.filter(korean_name=user.username).first()
    if not member:
        member = ChurchMember.objects.filter(email=user.email).first()
    
    if member:
        print(f'교인: {member.korean_name} ({member.member_id})')
        print(f'이메일: {member.email}')
        print(f'헌금봉투: {member.offering_number}')
        
        # 헌금 내역
        offerings = Offering.objects.filter(member=member).order_by('-offering_date')
        print(f'\n=== 헌금 내역 ===')
        print(f'총 {offerings.count()}건')
        for o in offerings:
            print(f'  - {o.offering_date} / {o.offering_type.name} / {o.amount:,}원 / {o.notes}')
    else:
        print('교인 정보 없음')
        
except User.DoesNotExist:
    print('사용자를 찾을 수 없습니다.')
