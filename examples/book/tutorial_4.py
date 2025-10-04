from mcp.server.fastmcp import FastMCP, Image
from PIL import Image as PILImage
import os
import tempfile

mcp = FastMCP(name = 'tutorial_4')

@mcp.tool()
def create_thumbnail() -> Image:
    '''
    Create a thumbnail image.
    '''
    try:
        img_path = "/Users/auaicn/projects/mcp-server-practice/sample-image.jpg"
        img = PILImage.open(img_path)
        img.thumbnail((100, 100))

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            img.save(tmp, format="png")
            tmp_path = tmp.name

        return Image(tmp_path, format="png")
    except Exception as e:
        return f"Error creating thumbnail: {e}"

if __name__ == "__main__":
    mcp.run()