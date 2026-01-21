from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import redirect
from offerings.models import TaxCertificateIssueLog
import csv

@staff_member_required
def reset_certificate_issuelog(request):
    if request.method == 'POST':
        TaxCertificateIssueLog.objects.all().delete()
        return redirect('budget:statistics_dashboard')
    return HttpResponse(status=405)

@staff_member_required
def backup_certificate_issuelog(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="certificate_issuelog_backup.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'member', 'issued_at', 'year', 'amount', 'etc'])
    for log in TaxCertificateIssueLog.objects.all():
        writer.writerow([
            log.id,
            getattr(log.member, 'name', ''),
            log.issued_at,
            log.year,
            log.amount,
            getattr(log, 'etc', '')
        ])
    return response
