from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Sum
from django.contrib import messages
from django.http import HttpResponse
from .models import BudgetTransaction, AnnualBudget
from .forms import ExpenseRequestForm
from .decorators import staff_member_required
from .pdf_utils import generate_expense_report_pdf
from .excel_utils import create_expense_excel, create_budget_excel

@login_required
def expense_request(request):
    """지출 신청 작성 뷰"""
    if request.method == 'POST':
        form = ExpenseRequestForm(request.POST, request.FILES, user=request.user)
        
        if form.is_valid():
            expense = form.save(commit=False)
            expense.requester = request.user
            expense.save()
            messages.success(request, '지출 신청이 성공적으로 접수되었습니다.')
            return redirect('budget:expense_request_list')
    else:
        form = ExpenseRequestForm(user=request.user)
    
    return render(request, 'budget/expense_request.html', {'form': form})

@login_required
def expense_request_list(request):
    """나의 지출 신청 목록 (컨텍스트 변수명 일치)"""
    expenses = BudgetTransaction.objects.filter(requester=request.user).order_by('-created_at')
    # 통계용 변수 추가
    total_count = expenses.count()
    pending_count = expenses.filter(status='pending').count()
    approved_count = expenses.filter(status='approved').count()
    total_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    from django.utils import timezone
    current_year = timezone.now().year
    
    return render(request, 'budget/expense_request_list.html', {
        'expenses': expenses,
        'total_count': total_count,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'total_amount': total_amount,
        'current_year': current_year,
    })

@login_required
def expense_request_detail(request, pk):
    """지출 신청 상세 보기"""
    expense = get_object_or_404(BudgetTransaction, pk=pk)
    
    # 본인 신청건이거나 관리자만 볼 수 있음
    if not request.user.is_staff and expense.requester != request.user:
        messages.error(request, "조회 권한이 없습니다. 관리자에게 문의하세요010-8921-9973")
        return redirect('budget:expense_request_list')
    
    # 영수증 업로드 처리
    if request.method == 'POST' and 'receipt' in request.FILES:
        expense.receipt = request.FILES['receipt']
        expense.save()
        messages.success(request, "영수증이 업로드되었습니다.")
        return redirect('budget:expense_request_detail', pk=pk)
        
    return render(request, 'budget/expense_request_detail.html', {'expense': expense})
 
@login_required
@staff_member_required
def approval_dashboard(request):
    """결재 대시보드 (관리자용)"""
    pending_expenses = BudgetTransaction.objects.filter(status='pending').order_by('created_at')
    
    stats = {
        'pending_count': pending_expenses.count(),
        'total_amount': pending_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    }
    
    return render(request, 'budget/approval_dashboard.html', {
        'pending_expenses': pending_expenses,
        'stats': stats
    })

@require_POST
@login_required
@staff_member_required
def approve_expense(request, request_id):
    """지출 승인 처리"""
    expense = get_object_or_404(BudgetTransaction, id=request_id)
    
    if expense.budget.balance < expense.amount:
        messages.error(request, f"예산 잔액 부족으로 '{expense.description}' 건을 승인할 수 없습니다. (잔액: {expense.budget.balance}원)")
        return redirect('budget:approval_dashboard')
        
    expense.status = 'approved'
    expense.approved_by = request.user
    expense.approved_at = timezone.now()
    expense.save()
    messages.success(request, f"'{expense.description}' 건이 승인되었습니다.")
    return redirect('budget:approval_dashboard')

@require_POST
@login_required
@staff_member_required
def reject_expense(request, request_id):
    """지출 반려 처리"""
    expense = get_object_or_404(BudgetTransaction, id=request_id)
    rejection_reason = request.POST.get('rejection_reason', '').strip()
    
    if not rejection_reason:
        messages.error(request, "반려 사유를 입력해주세요.")
        return redirect('budget:approval_dashboard')
    
    expense.status = 'rejected'
    expense.approved_by = request.user  # 반려자 기록
    expense.approved_at = timezone.now()
    expense.rejection_reason = rejection_reason
    expense.save()
    messages.warning(request, f"'{expense.description}' 건이 반려되었습니다.")
    return redirect('budget:approval_dashboard')

@login_required
def download_expense_pdf(request, pk):
    """지출결의서 PDF 다운로드"""
    expense = get_object_or_404(BudgetTransaction, pk=pk)
    
    # 본인 신청건이거나 관리자만 다운로드 가능
    if not request.user.is_staff and expense.requester != request.user:
        messages.error(request, "다운로드 권한이 없습니다. 관리자에게 문의하세요010-8921-9973")
        return redirect('budget:expense_request_list')
    
    # PDF 생성
    pdf = generate_expense_report_pdf(expense)
    
    # HTTP 응답
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f'지출결의서_{expense.id}_{expense.transaction_date.strftime("%Y%m%d")}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

@login_required
@staff_member_required
def budget_performance_report(request):
    """예산 대비 실적 보고서 (AnnualBudget 신 구조에 맞게 쿼리 및 필드 접근 수정)"""
    current_year = timezone.now().year
    year = int(request.GET.get('year', current_year))
    budgets = AnnualBudget.objects.filter(year=year)
    budget_stats = []
    total_budget = 0
    total_spent = 0
    total_balance = 0
    for budget in budgets:
        spent = budget.spent_amount
        balance = budget.balance
        total_amt = budget.total_amount
        usage_rate = (float(spent) / float(total_amt) * 100) if total_amt else 0
        approved_count = budget.transactions.filter(status='approved').count()
        pending_count = budget.transactions.filter(status='pending').count()
        budget_stats.append({
            'budget': budget,
            'spent': spent,
            'balance': balance,
            'usage_rate': usage_rate,
            'approved_count': approved_count,
            'pending_count': pending_count,
        })
        total_budget += float(total_amt)
        total_spent += float(spent)
        total_balance += float(balance)
    total_usage_rate = (total_spent / total_budget * 100) if total_budget > 0 else 0
    available_years = list(range(current_year - 2, current_year + 3))
    context = {
        'year': year,
        'budget_stats': budget_stats,
        'total_budget': total_budget,
        'total_spent': total_spent,
        'total_balance': total_balance,
        'total_usage_rate': total_usage_rate,
        'available_years': available_years,
    }
    return render(request, 'budget/budget_performance_report.html', context)

@login_required
@staff_member_required
def export_expenses_excel(request):
    """지출 내역 Excel 내보내기"""
    # 필터 파라미터
    year = request.GET.get('year')
    month = request.GET.get('month')
    status = request.GET.get('status')
    department = request.GET.get('department')
    
    # 쿼리셋 필터링
    transactions = BudgetTransaction.objects.all().select_related('budget', 'requester', 'approved_by').order_by('-transaction_date')
    
    filters = {}
    
    if year:
        transactions = transactions.filter(transaction_date__year=year)
        filters['연도'] = f'{year}년'
    
    if month:
        transactions = transactions.filter(transaction_date__month=month)
        filters['월'] = f'{month}월'
    
    if status:
        transactions = transactions.filter(status=status)
        status_map = {'pending': '대기', 'approved': '승인', 'rejected': '반려'}
        filters['상태'] = status_map.get(status, status)
    
    if department:
        transactions = transactions.filter(budget__department_name=department)
        filters['부서'] = department
    
    # Excel 생성
    excel_data = create_expense_excel(transactions, filters)
    
    # 응답
    response = HttpResponse(
        excel_data,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    filename = f'지출내역_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

@login_required
@staff_member_required
def export_budget_excel(request):
    """예산 현황 Excel 내보내기"""
    year = request.GET.get('year', timezone.now().year)
    
    budgets = AnnualBudget.objects.filter(year=year).prefetch_related('transactions')
    
    # Excel 생성
    excel_data = create_budget_excel(budgets, year)
    
    # 응답
    response = HttpResponse(
        excel_data,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    filename = f'{year}년_예산현황_{timezone.now().strftime("%Y%m%d")}.xlsx'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

@login_required
@staff_member_required
def statistics_dashboard(request):
    """통계 대시보드"""
    from offerings.models import Offering, OfferingType
    from django.db.models import Q
    import json
    
    # 연도 선택
    current_year = timezone.now().year
    year = int(request.GET.get('year', current_year))
    
    # 월별 데이터 수집
    monthly_data = []
    monthly_offerings = []
    monthly_expenses = []
    monthly_labels = []
    
    total_offering = 0
    total_expense = 0
    offering_count = 0
    expense_count = 0
    
    for month in range(1, 13):
        # 헌금
        month_offerings = Offering.objects.filter(
            offering_date__year=year,
            offering_date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # 지출 (승인된 것만)
        month_expenses = BudgetTransaction.objects.filter(
            transaction_date__year=year,
            transaction_date__month=month,
            status='approved'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        balance = month_offerings - month_expenses
        
        monthly_data.append({
            'month': month,
            'offering': month_offerings,
            'expense': month_expenses,
            'balance': balance
        })
        
        monthly_offerings.append(float(month_offerings))
        monthly_expenses.append(float(month_expenses))
        monthly_labels.append(f'{month}월')
        
        total_offering += month_offerings
        total_expense += month_expenses
    
    offering_count = Offering.objects.filter(offering_date__year=year).count()
    expense_count = BudgetTransaction.objects.filter(
        transaction_date__year=year,
        status='approved'
    ).count()
    
    # 헌금 유형별 통계
    offering_types = OfferingType.objects.all()
    offering_type_stats = []
    offering_type_labels = []
    offering_type_values = []
    
    for otype in offering_types:
        amount = Offering.objects.filter(
            offering_date__year=year,
            offering_type=otype
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        if amount > 0:
            offering_type_labels.append(otype.name)
            offering_type_values.append(float(amount))
    
    # 부서별 지출 통계
    departments = AnnualBudget.objects.filter(year=year).values('department_name').distinct()
    department_labels = []
    department_values = []
    
    for dept in departments:
        dept_name = dept['department_name']
        amount = BudgetTransaction.objects.filter(
            budget__year=year,
            budget__department_name=dept_name,
            status='approved'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        if amount > 0:
            department_labels.append(dept_name)
            department_values.append(float(amount))
    
    # 대기 중인 신청
    pending_count = BudgetTransaction.objects.filter(status='pending').count()
    pending_amount = BudgetTransaction.objects.filter(status='pending').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # 연도 목록
    available_years = list(range(current_year - 2, current_year + 3))
    
    context = {
        'year': year,
        'monthly_data': monthly_data,
        'monthly_labels': json.dumps(monthly_labels),
        'monthly_offerings': json.dumps(monthly_offerings),
        'monthly_expenses': json.dumps(monthly_expenses),
        'offering_type_labels': json.dumps(offering_type_labels),
        'offering_type_values': json.dumps(offering_type_values),
        'department_labels': json.dumps(department_labels),
        'department_values': json.dumps(department_values),
        'total_offering': total_offering,
        'total_expense': total_expense,
        'balance': total_offering - total_expense,
        'offering_count': offering_count,
        'expense_count': expense_count,
        'pending_count': pending_count,
        'pending_amount': pending_amount,
        'available_years': available_years,
        'user': request.user,
    }
    return render(request, 'budget/statistics_dashboard.html', context)
