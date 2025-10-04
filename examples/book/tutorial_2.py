from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name = 'tutorial_2')

@mcp.tool()
def add(a: int, b: int) -> int:
    '''
    입력받은 두 수를 더합니다.
    '''
    return a + b

@mcp.resource('greeting://hello')
def get_greeting() -> str:
    '''
    인사말을 제공하는 함수
    '''
    return "Hello, world!"

if __name__ == "__main__":
    mcp.run()