from mcp.server.fastmcp import FastMCP
from typing import Any, cast, Callable

def _setup_stdio_transport(mcp_server: FastMCP, **kwargs:Any) -> None:
    """
    Setup the stdio transport for the FastMCP server.
    This function is used to initialize the transport layer for the FastMCP server.
    """

    try:
        print("Setting up stdio transport...")
        getattr(mcp_server, 'run_stdio_async')
    except AttributeError:
        raise RuntimeError("Transport layer not initialized. Please call initialize_transport() first.")

def _get_transport_handler(transport_type: str) -> Any:
    """
    Get the transport handler based on the transport type.
    """

    transport_handlers ={
        'stdio': _setup_stdio_transport
    }
    if transport_type not in transport_handlers:
        supported_types = ', '.join(transport_handlers.keys())
        raise ValueError(f"Unsupported transport type: {transport_type}. Supported types are: {supported_types}")
    handler = cast(Callable[[FastMCP], None],
                   transport_handlers[transport_type])
    return handler
    

def initialize_transport(mcp_server : FastMCP, transport_type: str, transport_config: dict[str,Any]) -> None:
    """
    Initialize the transport layer.
    Args:
        mcp_server (FastMCP): The FastMCP server instance.
        transport_type (str): The type of transport to use (e.g., 'stdio').
        transport_config (dict[str, Any]): Configuration for the transport layer.
    """
    handler = _get_transport_handler(transport_type)

    try:
        handler(mcp_server, **transport_config)
    except Exception as e:  
        raise RuntimeError(f"Failed to initialize transport: {e}") from e


