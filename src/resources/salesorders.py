from typing import Optional, Any

from utils.api import zoho_api_request


def list_sales_orders(page: int = 1, per_page: int = 100, search_text: Optional[str] = None, sort_column: str = "date") -> dict[str, Any]:
    """
    List all sales orders in the Zoho Inventory account.

    Args:
        page (int): The page number to retrieve for pagination.
        per_page (int): The number of items per page.
        search_text (str, optional): The text to filter items by name and description.
        sort_column (str): The column to sort by(date, customer_name).

    Returns:
        dict[str, Any]: A dictionary containing the list of sales orders and pagination information.
    """

    params = {
        "page": page,
        "per_page": per_page,
        "sort_column": sort_column,
    }
    if search_text:
        params["search_text"] = search_text
    try:
        response = zoho_api_request("GET", "/salesorders", params=params)
        result = {
            "page": page,
            "per_page": per_page,
            "has_more_page": response.get("page_context", {}).get("has_more_page", False),
            "sales_orders": response.get("salesorders", []),
            "message": response.get("message", ""),
        }
        if "page_context" in response and "total" in response["page_context"]:
            result["total"] = response["page_context"]["total"]
        return result
    except Exception as e:
        print(f"Error listing sales orders: {e}")

def get_salesorder(salesorder_id: str) -> dict[str, Any]:
    """
    Get a sales order by ID.

    Args:
        salesorder_id (str): The ID of the sales order to retrieve.

    Returns:
        dict[str, Any]: A dictionary containing the sales order details.
    """
    if not isinstance(salesorder_id, str):
        raise ValueError("salesorder_id must be a string")
    try:
        response = zoho_api_request("GET", f"/salesorders/{salesorder_id}")
        result = {
            "sales_order": response.get("salesorder", {}),
            "message": response.get("message", ""),
        }
        return result
    except Exception as e:
        print(f"Error getting sales order: {e}")
        return None