import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'church_finance.settings')
django.setup()

from django.contrib.auth.models import User
from members.models import ChurchMember
from offerings.models import Offering

print('=== 모든 사용자 ===')
for u in User.objects.all():
    print(f'- {u.username} / 이메일: {u.email}')

print('\n=== 모든 교인 ===')
for m in ChurchMember.objects.all():
    print(f'- {m.korean_name} ({m.member_id}) / 이메일: {m.email} / 봉투: {m.offering_number}')

print('\n=== 모든 헌금 ===')
for o in Offering.objects.all():
    print(f'- {o.member.korean_name} / {o.offering_type.name} / {o.amount}원 / {o.offering_date}')

print('\n=== 사용자와 교인 매칭 확인 ===')
for u in User.objects.all():
    # 이메일로 찾기
    member = ChurchMember.objects.filter(email=u.email).first()
    if not member:
        # 이름으로 찾기
        member = ChurchMember.objects.filter(korean_name=u.username).first()
    
    if member:
        print(f'✓ {u.username} → {member.korean_name}')
    else:
        print(f'✗ {u.username} → 교인 정보 없음')
