from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name = 'server')

@mcp.tool()
def add(a: int, b: int) -> int:
    """Get a book by title"""
    return a + b

if __name__ == "__main__":
    mcp.run()