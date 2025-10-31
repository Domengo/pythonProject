from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
async def hello(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)