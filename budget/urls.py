# budget/urls.py
from django.urls import path
from . import views
from . import admin_certificate_tools
from . import admin_db_backup
from . import admin_full_backup
from . import admin_tools_view
from . import admin_data_reset

app_name = 'budget'

urlpatterns = [
    # 지출 신청 관련
    path('expense/request/', views.expense_request, name='expense_request'),
    path('expense/requests/', views.expense_request_list, name='expense_request_list'),
    path('expense/request/<int:pk>/', views.expense_request_detail, name='expense_request_detail'),
    path('expense/request/<int:pk>/pdf/', views.download_expense_pdf, name='download_expense_pdf'),
    
    # 결재 관련
    path('approval/dashboard/', views.approval_dashboard, name='approval_dashboard'),
    path('expense/request/<int:request_id>/approve/', views.approve_expense, name='approve_expense'),
    path('expense/request/<int:request_id>/reject/', views.reject_expense, name='reject_expense'),
    
    # 보고서
    path('report/performance/', views.budget_performance_report, name='budget_performance_report'),
    path('report/statistics/', views.statistics_dashboard, name='statistics_dashboard'),
    
    # Excel 내보내기
    path('export/expenses/', views.export_expenses_excel, name='export_expenses_excel'),
    path('export/budget/', views.export_budget_excel, name='export_budget_excel'),
    # 증명서 발급현황 초기화/백업
    path('certificate/reset/', admin_certificate_tools.reset_certificate_issuelog, name='reset_certificate_issuelog'),
    path('certificate/backup/', admin_certificate_tools.backup_certificate_issuelog, name='backup_certificate_issuelog'),
    # DB 전체 백업
    path('db/backup/', admin_db_backup.backup_sqlite_db, name='backup_sqlite_db'),
    # DB+media 전체 백업
    path('full/backup/', admin_full_backup.backup_db_and_media, name='backup_db_and_media'),
    # 관리자 도구
    path('admin/tools/', admin_tools_view.admin_tools, name='admin_tools'),
    # 데이터 초기화
    path('admin/data-reset/', admin_data_reset.admin_data_reset, name='admin_data_reset'),
]