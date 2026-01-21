import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'church_finance.settings')
django.setup()

from django.contrib.auth.models import User
from members.models import ChurchMember
from offerings.models import Offering

print('=== sal0421 확인 ===')
sal = User.objects.get(username='sal0421')
print(f'사용자: {sal.username}')
print(f'이메일: {sal.email}')

print('\n=== 김기철 확인 ===')
kim = ChurchMember.objects.get(member_id='001')
print(f'교인: {kim.korean_name}')
print(f'이메일: {kim.email}')
print(f'봉투번호: {kim.offering_number}')

print(f'\n=== 이메일 일치 여부 ===')
print(f'{sal.email} == {kim.email} : {sal.email == kim.email}')

print('\n=== 김기철 헌금 ===')
offerings = Offering.objects.filter(member=kim)
print(f'개수: {offerings.count()}')
for o in offerings:
    print(f'  - {o.offering_type.name}: {o.amount}원 ({o.offering_date})')
