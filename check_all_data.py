import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'church_finance.settings')
django.setup()

from django.contrib.auth.models import User
from members.models import ChurchMember
from offerings.models import Offering

# 모든 사용자 확인
print('=== 모든 사용자 ===')
users = User.objects.all()
for u in users:
    print(f'{u.id}. {u.username} - {u.email}')

# 모든 교인 확인
print('\n=== 모든 교인 ===')
members = ChurchMember.objects.all()
for m in members:
    print(f'{m.member_id}. {m.korean_name} - {m.email} - 봉투:{m.offering_number}')

# 모든 헌금 확인
print('\n=== 모든 헌금 ===')
offerings = Offering.objects.all()
for o in offerings:
    print(f'{o.id}. {o.member.korean_name} - {o.offering_type.name} - {o.amount:,}원 - {o.offering_date}')
