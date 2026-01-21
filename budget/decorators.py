from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

def staff_member_required(view_func):
    """
    사용자가 스태프 멤버인지 확인하는 데코레이터.
    스태프가 아니면 'dashboard'로 리디렉션하고 오류 메시지를 표시합니다.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "해당 페이지의 접근 권한이 없습니다. 관리자에게 문의하세요010-8921-9973", extra_tags='blink')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view