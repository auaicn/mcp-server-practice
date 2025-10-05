from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="data_extractor")

@mcp.prompt()
def extract_data(
    target: str,
    data_type: str,
    output_format: str = "csv"  # 기본값도 가능
) -> str:
    """
    연결 대상, 추출할 데이터, 출력 형식을 받아서
    추출 지시문을 생성합니다.
    """
    if output_format.lower() not in ("csv", "excel", "pdf"):
        return "출력 형식은 csv, excel, pdf 중 하나를 선택해주세요."

    return f"""
다음 조건으로 데이터를 추출해주세요:

- 연결 대상: {target}
- 추출 데이터: {data_type}
- 출력 형식: {output_format.upper()}

실행 시 다음과 같은 절차를 따릅니다.
1. '{target}'에 연결합니다.
2. '{data_type}' 데이터를 조회합니다.
3. 결과를 '{output_format.upper()}' 형식으로 내보냅니다.
"""

if __name__ == "__main__":
    mcp.run()
