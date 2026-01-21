from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from members.models import ChurchMember
from offerings.models import Offering, TaxCertificateIssueLog
from budget.models import BudgetTransaction

@staff_member_required
def admin_data_reset(request):
    if request.method == 'POST':
        # 실제 데이터 삭제
        ChurchMember.objects.all().delete()
        Offering.objects.all().delete()
        TaxCertificateIssueLog.objects.all().delete()
        BudgetTransaction.objects.all().delete()
        messages.success(request, '모든 교인/헌금/지출/증명서 데이터가 초기화되었습니다.')
        return redirect(reverse('budget:admin_tools'))
    return render(request, 'budget/admin_data_reset_confirm.html')
