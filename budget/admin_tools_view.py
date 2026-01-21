from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

def admin_tools(request):
    return render(request, 'admin_tools.html')
