from django.contrib import admin
from .models import ChurchMember

@admin.register(ChurchMember)
class ChurchMemberAdmin(admin.ModelAdmin):
    list_display = ['member_id', 'korean_name', 'phone', 'department', 'status']
    list_filter = ['status', 'department', 'gender']
    search_fields = ['korean_name', 'member_id', 'phone']
    list_per_page = 50
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('member_id', 'korean_name', 'english_name', 
                      'gender', 'birth_date', 'baptism_date')
        }),
        ('가족 정보', {
            'fields': ('family_id', 'relationship')
        }),
        ('연락처', {
            'fields': ('phone', 'email', 'address')
        }),
        ('교회 정보', {
            'fields': ('department', 'position', 'status')
        }),
        ('헌금 정보', {
            'fields': ('offering_number', 'tax_issuance_consent')
        }),
        ('기타', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # 자동으로 교인번호 생성
        if not obj.member_id:
            last_member = ChurchMember.objects.order_by('-created_at').last()
            if last_member and last_member.member_id and last_member.member_id.startswith('M'):
                try:
                    last_num = int(last_member.member_id[1:])
                    new_id = last_num + 1
                except:
                    new_id = 1
            else:
                new_id = 1
            obj.member_id = f"M{new_id:04d}"
        super().save_model(request, obj, form, change)