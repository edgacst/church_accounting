import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'church_finance.settings')
django.setup()

from budget.models import AnnualBudget

def create_initial_data():
    """
    현재 연도에 대한 초기 AnnualBudget 데이터를 생성합니다.
    """
    current_year = date.today().year
    
    departments = [
        {'name': '예배부', 'amount': 5000000},
        {'name': '교육부', 'amount': 10000000},
        {'name': '선교부', 'amount': 7000000},
        {'name': '청년부', 'amount': 3000000},
        {'name': '관리부', 'amount': 12000000},
    ]
    
    for dept in departments:
        budget, created = AnnualBudget.objects.get_or_create(
            year=current_year,
            department_name=dept['name'],
            defaults={
                'total_amount': dept['amount'],
                'is_approved': True
            }
        )
        if created:
            print(f"✓ {current_year}년 {dept['name']} 예산 생성 완료 (금액: {dept['amount']})")
        else:
            print(f"✓ {current_year}년 {dept['name']} 예산이 이미 존재합니다.")
    
    print("\n✅ 예산 관리 시스템 초기 데이터 생성 완료!")

if __name__ == '__main__':
    create_initial_data()