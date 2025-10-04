from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name = 'tutorial_3')

@mcp.prompt()
def prompt_extension(contents: str) -> str:
    """프롬프트에서 사실과 의견을 구분합니다."""
    return f"""{contents}
    
이 프롬프트에 대해 아래와 같은 템플릿에 맞춰 답변해줘.

* 사실:

* 의견:
"""

if __name__ == "__main__":
    mcp.run()