from fastmcp import FastMCP

mcp=FastMCP(name="expense tracking server")

@mcp.tool
def create_expense():
     pass