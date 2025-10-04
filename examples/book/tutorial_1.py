from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name = 'tutorial_1')

@mcp.tool()
def echo(message: str) -> str:
    '''
    입력받은 텍스트를 그대로 반환합니다.
    '''
    return message + " 라는 메시지가 입력되었습니다."

if __name__ == "__main__":
    mcp.run()