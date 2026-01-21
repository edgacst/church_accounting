import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'church_finance.settings')
django.setup()

from members.models import ChurchMember
from offerings.models import Offering, OfferingType

# 이승아 교인 다시 생성
lee, created = ChurchMember.objects.get_or_create(
    member_id='000002',
    defaults={
        'korean_name': '이승아',
        'phone': '010-2222-3333',
        'email': 'admin@church.local',
        'offering_number': '000002'
    }
)

if created:
    print(f'✓ 이승아 교인 생성 완료!')
else:
    print(f'✓ 이승아 교인 이미 존재 - 이메일 업데이트')
    lee.email = 'admin@church.local'
    lee.save()

# 감사헌금 유형 확인
thanks_type, _ = OfferingType.objects.get_or_create(
    code='THANKS',
    defaults={'name': '감사헌금'}
)

# 이승아 헌금 다시 생성
offering, created = Offering.objects.get_or_create(
    member=lee,
    offering_type=thanks_type,
    offering_date='2026-01-15',
    defaults={
        'amount': 100000,
        'is_confirmed': True
    }
)

if created:
    print(f'✓ 이승아 헌금 생성 완료!')
else:
    print(f'✓ 이승아 헌금 이미 존재')

print(f'\n최종 확인:')
print(f'이승아: {lee.korean_name} - {lee.email}')
print(f'헌금: {offering.offering_type.name} - {offering.amount}원')
