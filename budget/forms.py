from django import forms
from .models import BudgetTransaction, AnnualBudget
from django.utils import timezone

class ExpenseRequestForm(forms.ModelForm):
    """지출 신청 폼"""
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # 현재 연도의 예산만 필터링
        if user:
            current_year = timezone.now().year
            self.fields['budget'].queryset = AnnualBudget.objects.filter(
                year=current_year
            )
    
    class Meta:
        model = BudgetTransaction
        fields = [
            'budget',
            'transaction_date',
            'amount',
            'description',
            'vendor',
            'notes',
            'receipt',
        ]
        widgets = {
            'transaction_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
        labels = {
            'budget': '사용 예산',
            'transaction_date': '지출 일자',
            'amount': '금액',
            'description': '지출 내용',
            'vendor': '거래처',
            'notes': '비고',
            'receipt': '영수증 이미지',
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError("금액은 0보다 커야 합니다.")
        return amount

    def clean_transaction_date(self):
        transaction_date = self.cleaned_data.get('transaction_date')
        if transaction_date and transaction_date > timezone.now().date():
            raise forms.ValidationError("지출 일자는 미래 날짜일 수 없습니다.")
        return transaction_date