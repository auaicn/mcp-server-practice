from mcp.server.fastmcp import FastMCP
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
from typing import Optional

mcp = FastMCP(name="ipo_analyzer")

@mcp.tool()
def get_ipo_data(company_name: Optional[str] = None) -> str:
    """
    38커뮤니케이션 사이트에서 공모주 데이터를 가져옵니다.
    
    Args:
        company_name: 특정 기업명 (None이면 첫 페이지의 모든 공모주 정보 반환)
    """
    try:
        url = "https://www.38.co.kr/html/fund/index.htm?o=r"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 공모주 정보가 있는 테이블 찾기
        tables = soup.find_all('table')
        ipo_data = []
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 3:  # 최소 3개 컬럼이 있는 행만 처리
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    if any(keyword in ' '.join(row_data).lower() for keyword in ['기업명', '공모가', '상장일', '공모주']):
                        ipo_data.append(row_data)
        
        if company_name:
            # 특정 기업 검색
            filtered_data = []
            for data in ipo_data:
                if company_name.lower() in ' '.join(data).lower():
                    filtered_data.append(data)
            
            if filtered_data:
                result = f"'{company_name}' 관련 공모주 정보:\n\n"
                for data in filtered_data:
                    result += " | ".join(data) + "\n"
            else:
                result = f"'{company_name}'에 대한 공모주 정보를 찾을 수 없습니다.\n\n"
                result += "현재 진행 중인 공모주 목록:\n"
                for data in ipo_data[:10]:  # 상위 10개만 표시
                    result += " | ".join(data) + "\n"
        else:
            # 모든 공모주 정보 반환
            result = "현재 진행 중인 공모주 목록:\n\n"
            for data in ipo_data[:20]:  # 상위 20개만 표시
                result += " | ".join(data) + "\n"
        
        return result
        
    except Exception as e:
        return f"데이터를 가져오는 중 오류가 발생했습니다: {str(e)}"

@mcp.tool()
def get_securities_report(company_name: str) -> str:
    """
    DART에서 특정 기업의 증권신고서를 검색합니다.
    
    Args:
        company_name: 기업명
    """
    try:
        # DART 공시서류검색 페이지
        search_url = "https://dart.fss.or.kr/dsab007/main.do"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 검색 파라미터 설정
        search_params = {
            'textCrpCik': company_name,
            'startDate': '',
            'endDate': '',
            'publicType': 'A001',  # 발행공시
            'reportType': 'A001',  # 증권신고(지분증권)
            'finalReport': 'recent',
            'maxResults': '100',
            'sort': 'date',
            'series': 'desc'
        }
        
        response = requests.get(search_url, params=search_params, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 검색 결과 테이블 찾기
        result_table = soup.find('table', {'class': 'tb_list'})
        if not result_table:
            return f"'{company_name}'에 대한 증권신고서를 찾을 수 없습니다."
        
        # 결과 파싱
        rows = result_table.find_all('tr')[1:]  # 헤더 제외
        reports = []
        
        for row in rows[:10]:  # 최근 10개만
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 4:
                report_data = {
                    'company': cells[1].get_text(strip=True),
                    'report_name': cells[2].get_text(strip=True),
                    'submitter': cells[3].get_text(strip=True),
                    'date': cells[4].get_text(strip=True)
                }
                reports.append(report_data)
        
        if reports:
            result = f"'{company_name}' 관련 증권신고서 목록:\n\n"
            for i, report in enumerate(reports, 1):
                result += f"{i}. {report['report_name']}\n"
                result += f"   - 제출인: {report['submitter']}\n"
                result += f"   - 접수일: {report['date']}\n\n"
            
            result += "\n※ 상세 내용은 DART 사이트에서 직접 확인하시기 바랍니다.\n"
            result += "※ 증권신고서에는 기업의 재무상태, 사업내용, 공모조건 등 상세 정보가 포함되어 있습니다."
        else:
            result = f"'{company_name}'에 대한 증권신고서를 찾을 수 없습니다."
        
        return result
        
    except Exception as e:
        return f"DART에서 데이터를 가져오는 중 오류가 발생했습니다: {str(e)}"

@mcp.prompt()
def analyze_ipo_investment(
    company_name: Optional[str] = None,
    business_description: str = "",
) -> str:
    """
    공모주 투자 여부에 대한 종합적인 분석을 제공합니다.
    
    Args:
        company_name: 공모주 기업명 (None이면 현재 진행 중인 공모주들 분석)
        business_description: 사업 설명 (선택사항)
    """
    
    if company_name:
        return f"""
다음 공모주에 대한 투자 의사결정 분석을 수행해주세요:

**기본 정보:**
- 기업명: {company_name}
- 사업 설명: {business_description if business_description else "제공되지 않음"}

**데이터 소스:**
1. 38커뮤니케이션 사이트 (https://www.38.co.kr/html/fund/index.htm?o=r)에서 최신 공모주 정보
2. DART 전자공시시스템 (https://dart.fss.or.kr/dsab007/main.do)에서 증권신고서 정보

**분석 요청 사항:**

1. **기업 분석**
   - 사업 모델 및 핵심 경쟁력 분석 (증권신고서의 사업내용 참조)
   - 재무제표 분석 (매출, 영업이익, 순이익 추이 - 증권신고서 재무정보 참조)
   - 업계 내 위치 및 성장성 평가
   - 리스크 요인 분석 (증권신고서의 위험요소 참조)

2. **공모주 평가**
   - 공모가격의 적정성 평가 (38커뮤니케이션 사이트 + 증권신고서 공모조건 참조)
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

**중요 참고사항:**
- 증권신고서에는 기업의 상세한 재무정보, 사업계획, 공모조건, 위험요소 등이 포함되어 있습니다.
- 공모가격, 발행주식수, 모집금액 등 정확한 공모 정보는 증권신고서에서 확인하세요.
- 기업의 재무상태와 사업성은 증권신고서의 재무제표와 사업보고서를 기반으로 분석하세요.

**출력 형식:**
- 각 섹션별로 명확한 제목과 내용 구분
- 수치 데이터는 표 형태로 정리
- 투자 의사결정은 명확한 결론과 근거 제시
- 리스크와 기회요소를 균형있게 분석

분석 결과는 투자자가 이해하기 쉽도록 구조화하여 제시해주세요.
"""
    else:
        return f"""
현재 진행 중인 공모주들에 대한 종합적인 분석을 수행해주세요:

**데이터 소스:**
1. 38커뮤니케이션 사이트 (https://www.38.co.kr/html/fund/index.htm?o=r)에서 최신 공모주 정보
2. DART 전자공시시스템 (https://dart.fss.or.kr/dsab007/main.do)에서 증권신고서 정보

**분석 요청 사항:**

1. **현재 공모주 현황**
   - 진행 중인 공모주 목록 및 기본 정보
   - 공모가격대별 분류 (증권신고서의 공모조건 참조)
   - 업종별 분포 분석

2. **투자 매력도 평가**
   - 각 공모주의 투자 매력도 점수 (1-10점)
   - 투자 우선순위 추천
   - 리스크 등급 분류 (증권신고서의 위험요소 참조)

3. **시장 분석**
   - 최근 공모주 시장 동향
   - 업종별 성과 분석
   - 시장 환경이 공모주에 미치는 영향

4. **투자 전략**
   - 공모주 투자 포트폴리오 구성 방안
   - 투자 시기 및 비중 권장사항
   - 주의해야 할 리스크 요인

**중요 참고사항:**
- 각 공모주의 상세 정보는 DART 증권신고서에서 확인하세요.
- 재무상태, 사업성, 공모조건 등은 증권신고서를 기반으로 분석하세요.
- 위험요소와 기회요소는 증권신고서의 위험공시를 참조하세요.

**출력 형식:**
- 각 섹션별로 명확한 제목과 내용 구분
- 수치 데이터는 표 형태로 정리
- 투자 의사결정은 명확한 결론과 근거 제시
- 리스크와 기회요소를 균형있게 분석

분석 결과는 투자자가 이해하기 쉽도록 구조화하여 제시해주세요.
"""

@mcp.tool()
def generate_ipo_report(
    company_name: Optional[str],
    analysis_content: str,
    output_filename: str = None
) -> str:
    """
    IPO 분석 결과를 PDF 보고서로 생성합니다.
    
    Args:
        company_name: 기업명 (None이면 전체 공모주 분석 보고서)
        analysis_content: 분석 내용
        output_filename: 출력 파일명 (선택사항)
    """
    
    if not output_filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if company_name:
            output_filename = f"IPO_Analysis_{company_name}_{timestamp}.pdf"
        else:
            output_filename = f"IPO_Market_Analysis_{timestamp}.pdf"
    
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
    if company_name:
        story.append(Paragraph(f"공모주 투자 분석 보고서", title_style))
    else:
        story.append(Paragraph(f"공모주 시장 분석 보고서", title_style))
    story.append(Spacer(1, 20))
    
    # 기본 정보 테이블
    basic_info = [
        ['항목', '내용'],
        ['분석일자', datetime.now().strftime("%Y년 %m월 %d일")],
        ['데이터 소스', '38커뮤니케이션 + DART 전자공시시스템'],
    ]
    
    if company_name:
        basic_info.insert(1, ['기업명', company_name])
    
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
    if company_name:
        story.append(Paragraph("투자 분석 결과", subtitle_style))
    else:
        story.append(Paragraph("시장 분석 결과", subtitle_style))
    
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
