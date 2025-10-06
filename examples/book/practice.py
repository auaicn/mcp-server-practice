from mcp.server.fastmcp import FastMCP
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import os

mcp = FastMCP(name="ipo_analyzer")

@mcp.prompt()
def analyze_ipo_investment(
    company_name: str,
    ipo_price: float,
    business_description: str = "",
) -> str:
    """
    공모주 투자 여부에 대한 종합적인 분석을 제공합니다.
    
    Args:
        company_name: 공모주 기업명
        ipo_price: 공모가격
        business_description: 사업 설명 (선택사항)
    """
    
    return f"""
다음 공모주에 대한 투자 의사결정 분석을 수행해주세요:
c
**기본 정보:**
- 기업명: {company_name}
- 공모가격: {ipo_price:,}원
- 사업 설명: {business_description if business_description else "제공되지 않음"}

**분석 요청 사항:**

1. **기업 분석**
   - 사업 모델 및 핵심 경쟁력 분석
   - 재무제표 분석 (매출, 영업이익, 순이익 추이)
   - 업계 내 위치 및 성장성 평가
   - 리스크 요인 분석

2. **공모주 평가**
   - 공모가격의 적정성 평가
   - 동종업계 기업들과의 밸류에이션 비교
   - 최근 유사 공모주 성과 분석
   - 상장 후 주가 전망

3. **투자 의사결정**
   - 투자 매력도 점수 (1-10점)
   - 투자 권고사항 (매수/중립/매도)
   - 투자 시 주의사항
   - 투자 비중 권장사항

4. **비교 분석**
   - 국내 유사 기업들과의 비교
   - 해외 유사 기업들과의 비교
   - 업계 평균 대비 평가

**출력 형식:**
- 각 섹션별로 명확한 제목과 내용 구분
- 수치 데이터는 표 형태로 정리
- 투자 의사결정은 명확한 결론과 근거 제시
- 리스크와 기회요소를 균형있게 분석

분석 결과는 투자자가 이해하기 쉽도록 구조화하여 제시해주세요.
"""

@mcp.tool()
def generate_ipo_report(
    company_name: str,
    ipo_price: float,
    analysis_content: str,
    output_filename: str = None
) -> str:
    """
    IPO 분석 결과를 PDF 보고서로 생성합니다.
    
    Args:
        company_name: 기업명
        ipo_price: 공모가격
        analysis_content: 분석 내용
        output_filename: 출력 파일명 (선택사항)
    """
    
    if not output_filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"IPO_Analysis_{company_name}_{timestamp}.pdf"
    
    # PDF 생성
    doc = SimpleDocTemplate(output_filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # 제목 스타일
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # 중앙 정렬
        textColor=colors.darkblue
    )
    
    # 부제목 스타일
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkgreen
    )
    
    # 내용 스타일
    content_style = ParagraphStyle(
        'CustomContent',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        leftIndent=20
    )
    
    # 제목
    story.append(Paragraph(f"공모주 투자 분석 보고서", title_style))
    story.append(Spacer(1, 20))
    
    # 기본 정보 테이블
    basic_info = [
        ['항목', '내용'],
        ['기업명', company_name],
        ['공모가격', f"{ipo_price:,}원"],
        ['분석일자', datetime.now().strftime("%Y년 %m월 %d일")],
    ]
    
    basic_table = Table(basic_info, colWidths=[2*inch, 4*inch])
    basic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(Paragraph("기본 정보", subtitle_style))
    story.append(basic_table)
    story.append(Spacer(1, 20))
    
    # 분석 내용
    story.append(Paragraph("투자 분석 결과", subtitle_style))
    
    # 분석 내용을 문단별로 나누어 처리
    paragraphs = analysis_content.split('\n\n')
    for para in paragraphs:
        if para.strip():
            # 제목인 경우 (## 또는 **로 시작)
            if para.strip().startswith('**') and para.strip().endswith('**'):
                title_text = para.strip().replace('**', '')
                story.append(Paragraph(title_text, subtitle_style))
            else:
                story.append(Paragraph(para.strip(), content_style))
            story.append(Spacer(1, 6))
    
    # 면책조항
    story.append(Spacer(1, 20))
    disclaimer = """
    <b>면책조항:</b><br/>
    본 보고서는 투자 참고용으로만 사용되어야 하며, 투자 권유가 아닙니다. 
    투자 결정은 개인의 판단과 책임하에 이루어져야 합니다. 
    과거 성과가 미래 수익을 보장하지 않으며, 투자에는 원금 손실 위험이 있습니다.
    """
    story.append(Paragraph(disclaimer, content_style))
    
    # PDF 생성
    doc.build(story)
    
    return f"PDF 보고서가 성공적으로 생성되었습니다: {output_filename}"

if __name__ == "__main__":
    mcp.run()
