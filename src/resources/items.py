
from typing import Optional, Any

from utils.api import zoho_api_request


def list_items(page:int = 1, per_page:int = 100, search_text: Optional[str] = None, sort_column: str = "name")-> dict[str, Any]:
    """
    List all items in the Zoho Inventory account.

    Args:
        page (int): The page number to retrieve for pagenation.
        per_page (int): The number of items per page.
        search_text (str, optional): The text to filter items by name and description.
        sort_column (str): The column to sort by(name, created_time, last_modified_time).

    Returns:
        dict[str, Any]: A dictionary containing the list of items and pagination information.
    """
    params = {
        "page": page,
        "per_page": per_page,
        "sort_column": sort_column,
    }
    if search_text:
        params["search_text"] = search_text

    try:
        response = zoho_api_request("GET", "/items", params=params)
        result = {
            "page": page,
            "per_page": per_page,
            "has_more_page": response.get("page_context", {}).get("has_more_page", False),
            "items": response.get("items", []),
            "message": response.get("message", ""),
        }

        if "page_context" in response and "total" in response["page_context"]:
            result["total"] = response["page_context"]["total"]

        return result
    except Exception as e:
        print (f"Error listing items: {e}")
        return None