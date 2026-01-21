# budget/pdf_utils.py
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from django.conf import settings
import os

def generate_expense_report_pdf(expense):
    """지출결의서 PDF 생성"""
    buffer = BytesIO()
    
    # PDF 문서 설정
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )
    
    # 한글 폰트 등록 (여러 경로 시도)
    font_name = 'Helvetica'  # 기본값
    font_paths = [
        "C:/Windows/Fonts/malgun.ttf",  # Windows - 맑은 고딕
        "C:/Windows/Fonts/gulim.ttc",   # Windows - 굴림
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",  # Linux - 나눔고딕
        "/usr/share/fonts/truetype/nanum/NanumMyeongjo.ttf",  # Linux - 나눔명조
        "/System/Library/Fonts/AppleGothic.ttf",  # macOS
        os.path.join(settings.BASE_DIR, "static", "fonts", "NanumGothic.ttf"),  # 프로젝트 폰트
    ]
    
    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('KoreanFont', font_path))
                font_name = 'KoreanFont'
                break
        except Exception as e:
            continue
    
    # 폰트를 찾지 못한 경우 경고 (선택사항)
    if font_name == 'Helvetica':
        import warnings
        warnings.warn("한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
    
    # 스타일 정의
    styles = getSampleStyleSheet()
    
    # 제목 스타일
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=18,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontWeight='bold'
    )
    
    # 본문 스타일
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        leading=14,
    )
    
    # 내용 구성
    elements = []
    
    # 제목
    title = Paragraph("지출 결의서", title_style)
    elements.append(title)
    elements.append(Spacer(1, 10*mm))
    
    # 문서 번호 및 날짜
    info_data = [
        ['문서번호', f'#{expense.id}', '작성일', expense.created_at.strftime('%Y년 %m월 %d일')],
    ]
    
    info_table = Table(info_data, colWidths=[30*mm, 50*mm, 30*mm, 50*mm])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#ecf0f1')),
        ('BACKGROUND', (2, 0), (2, 0), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 10*mm))
    
    # 지출 내역
    status_text = {
        'pending': '승인 대기',
        'approved': '승인됨',
        'rejected': '반려됨',
    }.get(expense.status, expense.status)
    
    # 신청자 이름 처리 (한글 이름이 있으면 사용, 없으면 username)
    requester_name = '-'
    if expense.requester:
        if expense.requester.last_name and expense.requester.first_name:
            requester_name = f'{expense.requester.last_name}{expense.requester.first_name}'
        elif expense.requester.first_name:
            requester_name = expense.requester.first_name
        else:
            requester_name = expense.requester.username
    
    # 결재자 이름 처리
    approver_name = '-'
    if expense.approved_by:
        if expense.approved_by.last_name and expense.approved_by.first_name:
            approver_name = f'{expense.approved_by.last_name}{expense.approved_by.first_name}'
        elif expense.approved_by.first_name:
            approver_name = expense.approved_by.first_name
        else:
            approver_name = expense.approved_by.username
    
    data = [
        ['항목', '내용'],
        ['지출 내용', expense.description],
        ['금액', f'{int(expense.amount):,}원'],
        ['지출 일자', expense.transaction_date.strftime('%Y년 %m월 %d일')],
        ['예산 항목', f'{expense.budget.year}년 {expense.budget.department_name}'],
        ['신청자', requester_name],
        ['거래처', expense.vendor or '-'],
        ['비고', expense.notes or '-'],
        ['결재 상태', status_text],
    ]
    
    if expense.approved_by:
        data.append(['결재자', approver_name])
    
    if expense.approved_at:
        data.append(['결재 일시', expense.approved_at.strftime('%Y년 %m월 %d일 %H:%M')])
    
    if expense.status == 'rejected' and expense.rejection_reason:
        data.append(['반려 사유', expense.rejection_reason])
    
    # 테이블 생성
    table = Table(data, colWidths=[40*mm, 120*mm])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#ecf0f1')),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('FONTWEIGHT', (0, 0), (-1, 0), 'BOLD'),
    ]))
    
    # 금액 행 강조
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#fff3cd')),
        ('FONTSIZE', (0, 2), (-1, 2), 12),
        ('FONTWEIGHT', (1, 2), (1, 2), 'BOLD'),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 20*mm))
    
    # 결재란
    approval_data = [
        ['신청', '부서장', '회계', '담임목사'],
        ['', '', '', ''],
        ['', '', '', ''],
    ]
    
    approval_table = Table(approval_data, colWidths=[40*mm, 40*mm, 40*mm, 40*mm], rowHeights=[10*mm, 20*mm, 10*mm])
    approval_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#95a5a6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTWEIGHT', (0, 0), (-1, 0), 'BOLD'),
    ]))
    
    elements.append(Paragraph("결  재", title_style))
    elements.append(Spacer(1, 5*mm))
    elements.append(approval_table)
    
    # 하단 문구
    elements.append(Spacer(1, 15*mm))
    footer_text = Paragraph(
        "위와 같이 지출을 신청합니다.<br/><br/>부평우리교회",
        ParagraphStyle('footer', parent=body_style, alignment=TA_CENTER, fontSize=9)
    )
    elements.append(footer_text)
    
    # PDF 생성
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf
