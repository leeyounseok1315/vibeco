from fastmcp import FastMCP

mcp = FastMCP("더하기")

@mcp.tool()
def add(a: int, b: int) -> int:
    """a와 b를 더하기"""
    return a + b

if __name__ == "__main__":
    mcp.run()
