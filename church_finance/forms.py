from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        from members.models import ChurchMember
        if ChurchMember.objects.filter(phone=phone).exists():
            raise forms.ValidationError('이미 등록된 연락처입니다. 관리자에게 문의하세요.')
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('이미 사용 중인 이메일입니다.')
        return email

    first_name = forms.CharField(
        required=True,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '이름(성 포함 전체 입력)'
        })
    )
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '비밀번호'
        }),
        help_text='8자 이상의 안전한 비밀번호를 입력하세요.'
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '비밀번호 확인'
        }),
        help_text='확인을 위해 같은 비밀번호를 다시 입력하세요.'
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': '이메일 주소'
        })
    )
    phone = forms.CharField(
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '연락처'
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'password1', 'password2', 'email', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = '이름'
        self.fields['password1'].label = '비밀번호'
        self.fields['password2'].label = '비밀번호 확인'
        self.fields['email'].label = '이메일'
        self.fields['phone'].label = '연락처'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # username을 email로 자동 할당
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        phone = self.cleaned_data['phone']
        if commit:
            user.save()
            from members.models import ChurchMember
            # 연락처로 ChurchMember 중복 체크 후, 없을 때만 생성
            member, created = ChurchMember.objects.get_or_create(phone=phone, defaults={
                'korean_name': user.first_name,
                'email': user.email,
                'user': user
            })
            if not created:
                # 이미 ChurchMember가 있으면 user 연결만 보장
                if not member.user:
                    member.user = user
                    member.email = user.email
                    member.korean_name = user.first_name
                    member.save()
        return user
