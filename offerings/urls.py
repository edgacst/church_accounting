from django.urls import path
from . import views

app_name = 'offerings'

urlpatterns = [
    path('certificates/', views.tax_certificate_list, name='tax_certificate_list'),
    path('certificate/<int:member_id>/', views.yearly_tax_certificate, name='yearly_tax_certificate'),
    path('certificate/<int:member_id>/<int:year>/', views.yearly_tax_certificate, name='yearly_tax_certificate_year'),
    path('certificate/<int:member_id>/<int:year>/log-print/', views.log_certificate_print, name='log_certificate_print'),
    path('export/offerings/', views.export_offerings_excel, name='export_offerings_excel'),
    path('export/offerings/<int:year>/', views.export_offerings_excel, name='export_offerings_excel_year'),
    path('export/members/', views.export_members_excel, name='export_members_excel'),
    path('export/tax-certificate/', views.export_tax_certificate_excel, name='export_tax_certificate_excel'),
    path('export/tax-certificate/<int:year>/', views.export_tax_certificate_excel, name='export_tax_certificate_excel_year'),
    path('list/', views.offering_list, name='offering_list'),
]