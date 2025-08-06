

from utils.api import zoho_api_request


def get_taxes(page: int = 1, per_page: int = 100):
    """
    Get all taxes in the Zoho Inventory account.
    Args:
        page (int): The page number to retrieve for pagination.
        per_page (int): The number of items per page.
    Returns:
        dict[str, Any]: A dictionary containing the list of taxes and pagination information.
    """
    params = {
        "page": page,
        "per_page": per_page,
    }
    try:
        response = zoho_api_request("GET", "/settings/taxes", params=params)
        result = {
            "page": page,
            "per_page": per_page,
            "has_more_page": response.get("page_context", {}).get("has_more_page", False),
            "taxes": response.get("taxes", []),
            "message": response.get("message", ""),
        }
        if "page_context" in response and "total" in response["page_context"]:
            result["total"] = response["page_context"]["total"]
        return result
    except Exception as e:
        print(f"Error listing taxes: {e}")
