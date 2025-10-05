from mcp.server.fastmcp import FastMCP, Context
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

logger = logging.getLogger(__name__)

mcp = FastMCP(name = 'tutorial_5')

@mcp.tool()
async def greeting(name: str, ctx: Context) -> str:
    """Get a greeting using the greeting resource."""
    try:
        result = await ctx.read_resource(f"greeting://{name}")
        logger.debug(f"Result type: {type(result)}")
        logger.debug(f"Result: {result}")

        content = None

        if isinstance(result, list):
            content = result[0].content
        else:
            content = result.content
        
        if content is None:
            return f"Error getting greeting: {result}"
        
        return f"Tool Response : {content}"
    except Exception as e:
        return f"Error getting greeting: {e}"


@mcp.resource('greeting://{name}')
def get_greeting(name: str) -> str:
    """Get a greeting using the greeting resource."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()