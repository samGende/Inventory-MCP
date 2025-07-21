from typing import Optional, Any

from utils.api import zoho_api_request

def list_composite_items(page: int = 1, per_page: int = 100, search_text: Optional[str] = None, sort_column: str = "name") -> dict[str, Any]:
    """
    List all composite items in the Zoho Inventory account.

    Args:
        page (int): The page number to retrieve for pagination.
        per_page (int): The number of items per page.
        search_text (str, optional): The text to filter items by name and description.
        sort_column (str): The column to sort by(name, sku, rate, purchase_rate).

    Returns:
        dict[str, Any]: A dictionary containing the list of composite items and pagination information.
    """
    #TODO Should sort columns be validated all the time? 
    params = {
        "page": page,
        "per_page": per_page,
        "sort_column": sort_column,
    }
    if search_text:
        params["search_text"] = search_text

    try:
        response = zoho_api_request("GET", "/compositeitems", params=params)
        result = {
            "page": page,
            "per_page": per_page,
            "has_more_page": response.get("page_context", {}).get("has_more_page", False),
            "composite_items": response.get("composite_items", []),
            "message": response.get("message", ""),
        }

        if "page_context" in response and "total" in response["page_context"]:
            result["total"] = response["page_context"]["total"]

        return result
    except Exception as e:
        print(f"Error listing composite items: {e}")
        return None