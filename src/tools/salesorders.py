from typing import List, Dict, Any

from utils.api import zoho_api_request

def create_sales_order(customer_id: str, line_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create a sales order in Zoho Books.

    Args:
        customer_id (str): The ID of the customer.
        line_items (List[Dict[str, Any]]): A list of line items for the sales order.
            Required keys are:
                - item_id: The ID of the item.
                - quantity: The quantity of the item.
                - rate: The rate of the item.
                - item_total: The total amount for the item.
                - tax_id: The ID of the tax.

    Returns:
        Dict[str, Any]: The response from Zoho Books API.
    """
    #validate line_items
    if not isinstance(line_items, list):
        raise ValueError("line_items must be a list")
    for item in line_items:
        if not isinstance(item, dict):
            raise ValueError("Each line item must be a dictionary")
        required_keys = ["item_id", "quantity", "rate", "item_total", "tax_id"]
        for key in required_keys:
            if key not in item:
                raise ValueError(f"Missing required key '{key}' in line item")
            if key == "item_id":
                if not isinstance(item[key], str):
                    raise ValueError("item_id must be a string")
            elif key == "quantity":
                if not isinstance(item[key], (int, float)):
                    raise ValueError("quantity must be a number")
            elif key == "rate":
                if not isinstance(item[key], (int, float)):
                    raise ValueError("rate must be a number")
            elif key == "item_total":
                if not isinstance(item[key], (int, float)):
                    raise ValueError("item_total must be a number")
                if item[key] != item["quantity"] * item["rate"]:
                    raise ValueError("item_total must be equal to quantity * rate")
            elif key == "tax_id":
                if not isinstance(item[key], str):
                    raise ValueError("tax_id must be a string")                    

    data = {
        "customer_id": customer_id,
        "line_items": line_items,
    }

    try:
        response = zoho_api_request('POST', '/salesorders', json_data=data)
        result = {
            "sales_order": response.get("salesorder", {}),
            "message": response.get("message", ""),
        }
        return result
    except Exception as e:
        print(f"Error creating sales order: {e}")
        return None