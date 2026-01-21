from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChurchMember
from budget.models import BudgetTransaction
from offerings.models import Offering
from django.db.models import Sum, Q

@login_required
def my_page(request):
    """사용자 마이 페이지"""
    user = request.user
    
    # 사용자의 교인 정보 조회 (이메일 또는 이름으로)
    try:
        member = ChurchMember.objects.filter(
            Q(email=user.email) | Q(korean_name=user.username)
        ).first()
    except ChurchMember.DoesNotExist:
        member = None
    
    # 사용자의 지출 신청 내역
    my_transactions = BudgetTransaction.objects.filter(requester=user).order_by('-transaction_date')[:10]
    
    # 지출 신청 통계
    total_requested = BudgetTransaction.objects.filter(requester=user).aggregate(total=Sum('amount'))['total'] or 0
    approved_count = BudgetTransaction.objects.filter(requester=user, status='approved').count()
    pending_count = BudgetTransaction.objects.filter(requester=user, status='pending').count()
    rejected_count = BudgetTransaction.objects.filter(requester=user, status='rejected').count()
    
    # 내 헌금 내역 (교인 정보가 있는 경우)
    my_offerings = []
    total_offering = 0
    if member:
        my_offerings = Offering.objects.filter(member=member).order_by('-offering_date')[:10]
        total_offering = Offering.objects.filter(member=member).aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'member': member,
        'my_transactions': my_transactions,
        'total_requested': total_requested,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
        'my_offerings': my_offerings,
        'total_offering': total_offering,
    }
    
    return render(request, 'members/my_page.html', context)
