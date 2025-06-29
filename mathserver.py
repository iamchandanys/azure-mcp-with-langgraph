from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MathServer")

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Add two numbers together

    Args:
        a: The first number
        b: The second number

    Returns:
        The sum of the two numbers
    """
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """
    Subtract two numbers

    Args:
        a: The first number
        b: The second number

    Returns:
        The difference between the two numbers
    """
    return a - b

# Use standard input and output for the transport
if __name__ == "__main__":
    mcp.run(transport="stdio")
