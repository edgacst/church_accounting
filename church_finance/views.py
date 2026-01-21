from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from members.models import ChurchMember
from offerings.models import Offering, TaxCertificateIssueLog
from budget.models import BudgetTransaction
from django.utils import timezone
from datetime import timedelta
from .forms import SignupForm

@login_required
def dashboard(request):
    # 기본 통계
    total_members = ChurchMember.objects.count()
    active_members = ChurchMember.objects.filter(status='active').count()
    
    # 최근 30일 헌금 통계
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    recent_offerings = Offering.objects.filter(offering_date__gte=thirty_days_ago)
    
    total_offering_amount = sum([o.amount for o in recent_offerings])
    
    # 헌금 유형별 통계
    offering_by_type = {}
    for offering in recent_offerings:
        type_name = offering.offering_type.name
        offering_by_type[type_name] = offering_by_type.get(type_name, 0) + offering.amount
    
    # 증명서 발급 현황 (최근 30일)
    thirty_days_ago_datetime = timezone.now() - timedelta(days=30)
    certificate_logs = TaxCertificateIssueLog.objects.filter(
        issued_at__gte=thirty_days_ago_datetime
    )
    
    # 발급 유형별 집계
    certificate_stats = {
        'html_count': certificate_logs.filter(issue_type='html').count(),
        'pdf_count': certificate_logs.filter(issue_type='pdf').count(),
        'print_count': certificate_logs.filter(issue_type='print').count(),
    }
    certificate_stats['total_count'] = sum(certificate_stats.values())
    
    # 대기 중인 지출 신청 내역 (관리자인 경우)
    pending_expenses = []
    if request.user.is_staff:
        pending_expenses = BudgetTransaction.objects.filter(
            status='pending'
        ).select_related('requester', 'budget').order_by('-created_at')[:10]
    
    context = {
        'total_members': total_members,
        'active_members': active_members,
        'total_offering_amount': total_offering_amount,
        'offering_by_type': offering_by_type,
        'recent_offerings_count': recent_offerings.count(),
        'pending_expenses': pending_expenses,
        'certificate_stats': certificate_stats,
    }
    
    return render(request, 'dashboard.html', context)

def signup(request):
    """회원가입 뷰"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            from members.models import ChurchMember
            from uuid import uuid4
            korean_name = user.first_name
            email = user.email
            # ChurchMember가 이미 있으면 user 필드도 연결
            member, created = ChurchMember.objects.update_or_create(
                email=email,
                defaults={
                    'korean_name': korean_name,
                    'user': user,
                    'member_id': str(uuid4())[:20]
                }
            )
            # 혹시 user 필드가 연결 안 된 ChurchMember가 있으면 연결
            if not member.user:
                member.user = user
                member.save()
            messages.success(request, '회원가입이 완료되었습니다. 로그인해주세요.')
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})
