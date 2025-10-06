from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="data_extractor")

@mcp.prompt()
def extract_data(
    target: str,
    data_type: str,
) -> str:
    """
    기업명, 조사할 데이터를 받아서 데이터를 출력합니다.
    """

    return f"""
다음 조건으로 데이터를 추출해주세요:

- 연결 대상: {target}
- 추출 데이터: {data_type}

실행 시 다음과 같은 절차를 따릅니다.
- https://finance.naver.com/ 에서 데이터를 찾습니다.
- '{target}' 를 기업명으로 검색합니다.
- '{data_type}' 데이터를 조회합니다. 기본적으로 순 자본금등을 표로 정리하여 제시합니다.
- 삼성전자, 네이버 등 대표적인 국내 기업 평군과 비교가 필요하고
- 애플, 엔비디아 등의 해외기업과 비교가 필요합니다.
- 데이터는 표로 정리하여 제시합니다.
- 데이터는 최신 데이터를 제시합니다.
"""

if __name__ == "__main__":
    mcp.run()
