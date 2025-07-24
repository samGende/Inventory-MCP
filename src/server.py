from mcp.server.fastmcp import FastMCP

from tools.salesorders import create_sales_order, attach_pdf
from resources.salesorders import list_sales_orders, get_salesorder
from resources.taxes import get_taxes
from resources.items import list_items
from resources.contacts import list_contacts, get_contact
from resources.composite_items import list_composite_items
from transport import initialize_transport

def register_tools(mcp_server: FastMCP):
    mcp_server.add_tool(create_sales_order)
    mcp_server.add_tool(attach_pdf)

def register_resources(mcp_server: FastMCP):
    mcp_server.add_tool(list_sales_orders)
    mcp_server.add_tool(get_salesorder)
    mcp_server.add_tool(get_taxes)
    mcp_server.add_tool(list_items)
    mcp_server.add_tool(list_contacts)
    mcp_server.add_tool(get_contact)
    mcp_server.add_tool(list_composite_items)

def conigure_server(args: dict[str, str]):
    """configuer server based on args"""

    #configure logs 

    #configure cors

    #server config
    server_config={
        "name": "zoho-inventory",
        "verison": "1.0.0",
    }
    return server_config

def main():
    """
    main entroy point for mcp server 
    """

    #test the auth save in .env

    #start logs

    server_config = conigure_server(args={})

    #create mcp server
    mcp_server = FastMCP(**server_config)

    #register tools
    register_tools(mcp_server)
    #register resources
    register_resources(mcp_server)

    print('staring mcp server')

    mcp_server.run('stdio')

if __name__ == "__main__":
        main()