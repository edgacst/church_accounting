from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import AnnualBudget, BudgetTransaction

User = get_user_model()

class BudgetAppTestCase(TestCase):
    def setUp(self):
        """테스트를 위한 초기 데이터 설정"""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.staff_user = User.objects.create_user(username='staffuser', password='password123', is_staff=True)
        self.another_user = User.objects.create_user(username='anotheruser', password='password123')
        self.annual_budget = AnnualBudget.objects.create(
            year=2024,
            department_name="교육부",
            total_amount=1000000,
            is_approved=True
        )

    def test_expense_request_creation(self):
        """지출 신청 생성 테스트"""
        self.client.login(username='testuser', password='password123')
        
        initial_count = BudgetTransaction.objects.count()
        
        response = self.client.post(reverse('budget:expense_request'), {
            'budget': self.annual_budget.pk,
            'transaction_date': '2024-01-15',
            'amount': 50000,
            'description': '테스트 지출',
            'vendor': '테스트 거래처',
        })
        
        # 신청 후 리스트 페이지로 리다이렉트 되는지 확인
        self.assertRedirects(response, reverse('budget:expense_request_list'))
        
        # BudgetTransaction 객체가 1개 생성되었는지 확인
        self.assertEqual(BudgetTransaction.objects.count(), initial_count + 1)
        
        # 생성된 객체의 내용 확인
        transaction = BudgetTransaction.objects.first()
        self.assertEqual(transaction.requester, self.user)
        self.assertEqual(transaction.amount, 50000)
        self.assertEqual(transaction.status, 'pending')

    def test_approve_expense_flow(self):
        """지출 승인 및 예산 차감 테스트"""
        self.client.login(username='staffuser', password='password123')
        transaction = BudgetTransaction.objects.create(
            budget=self.annual_budget,
            requester=self.user,
            transaction_date='2024-01-20',
            amount=100000,
            description='승인 테스트'
        )
        
        initial_balance = self.annual_budget.balance
        self.assertEqual(initial_balance, 1000000)

        response = self.client.post(reverse('budget:approve_expense', args=[transaction.id]))
        self.assertRedirects(response, reverse('budget:approval_dashboard'))

        transaction.refresh_from_db()
        self.assertEqual(transaction.status, 'approved')
        self.assertEqual(transaction.approved_by, self.staff_user)

        self.annual_budget.refresh_from_db()
        self.assertEqual(self.annual_budget.balance, 900000)

    def test_reject_expense_flow(self):
        """지출 반려 테스트"""
        self.client.login(username='staffuser', password='password123')
        transaction = BudgetTransaction.objects.create(
            budget=self.annual_budget,
            requester=self.user,
            transaction_date='2024-01-21',
            amount=200000,
            description='반려 테스트'
        )

        response = self.client.post(reverse('budget:reject_expense', args=[transaction.id]))
        self.assertRedirects(response, reverse('budget:approval_dashboard'))

        transaction.refresh_from_db()
        self.assertEqual(transaction.status, 'rejected')
        self.assertEqual(self.annual_budget.balance, 1000000)

    def test_approve_expense_insufficient_balance(self):
        """예산 초과 시 지출 승인 실패 테스트"""
        self.client.login(username='staffuser', password='password123')
        transaction = BudgetTransaction.objects.create(
            budget=self.annual_budget,
            requester=self.user,
            transaction_date='2024-01-22',
            amount=1500000,
            description='예산 초과 테스트'
        )

        response = self.client.post(reverse('budget:approve_expense', args=[transaction.id]), follow=True)
        self.assertRedirects(response, reverse('budget:approval_dashboard'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f"예산 잔액 부족으로 '{transaction.description}' 건을 승인할 수 없습니다. (잔액: {self.annual_budget.balance}원)")

        transaction.refresh_from_db()
        self.assertEqual(transaction.status, 'pending')

    def test_non_staff_cannot_access_approval_views(self):
        """일반 사용자가 결재 관련 뷰에 접근 불가 테스트"""
        self.client.login(username='testuser', password='password123')
        
        # Dashboard
        response = self.client.get(reverse('budget:approval_dashboard'))
        self.assertRedirects(response, reverse('dashboard'))
        
        # Approve/Reject (POST)
        response = self.client.post(reverse('budget:approve_expense', args=[1]))
        self.assertRedirects(response, reverse('dashboard'))
