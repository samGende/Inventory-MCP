import pytest 

from resources.salesorders import list_sales_orders, get_salesorder
from tools.salesorders import create_sales_order, attach_pdf

def test_attach_pdf():
    salesorder_id = "5982345000000586002"  # Example sales order ID
    file_path = "./POs/#1182.pdf"  # Path to the PDF file to attach

    response = attach_pdf(salesorder_id, file_path)

    assert response is not None, "Response should not be None"
    assert isinstance(response, dict), "Response should be a dictionary"
    assert "message" in response, "Response should contain 'message' key"
    assert isinstance(response["message"], str), "'message' should be a string"
    assert "attached" in response["message"].lower(), "'message' should contain 'attachment added'"


def test_list_sales_orders():
    search_text = "Sam"

    response = list_sales_orders(page=1, per_page=10, search_text=search_text, sort_column="date")

    assert response is not None, "Response should not be None"
    assert isinstance(response, dict), "Response should be a dictionary"    
    assert "sales_orders" in response, "Response should contain 'sales_orders' key"
    assert isinstance(response["sales_orders"], list), "'sales_orders' should be a list"
    assert len(response["sales_orders"]) <= 10, f"'sales_orders' list should be less than 10 len is {len(response['sales_orders'])}"


    if len(response["sales_orders"]) > 0:
        item = response["sales_orders"][0]
        assert isinstance(item, dict), "Each item should be a dictionary"
        assert "customer_name" in item, "Each item should contain 'customer_name' key"
        assert search_text.lower() in item["customer_name"].lower(), f"Item name should contain '{search_text}'"

def test_get_salesorder():
    search_text = "Sam"

    response = list_sales_orders(page=1, per_page=10, search_text=search_text, sort_column="date")

    assert response is not None, "Response should not be None"
    assert isinstance(response, dict), "Response should be a dictionary"    
    assert "sales_orders" in response, "Response should contain 'sales_orders' key"

    salesorder = response["sales_orders"][0]
    salesorder_id = salesorder["salesorder_id"]
    assert salesorder_id is not None, "salesorder_id should not be None"
    assert isinstance(salesorder_id, str), "salesorder_id should be a string"

    response = get_salesorder(salesorder_id=salesorder_id)
    assert response is not None, "Response should not be None"
    assert isinstance(response, dict), "Response should be a dictionary"
    assert "sales_order" in response, "Response should contain 'sales_order' key"
    assert isinstance(response["sales_order"], dict), "'sales_order' should be a dictionary"
    assert "salesorder_id" in response["sales_order"], "'salesorder_id' should be in 'sales_order'"
    assert response["sales_order"]["salesorder_id"] == salesorder_id, "salesorder_id should match the one used in the request"

def test_create_sales_order():

    customer_id = "5982345000000135154"

    item = {'item_id': '5982345000000123546',
            'quantity': 2,
            'rate': 26.0,
            'item_total': 52.0,
            'tax_id': '5982345000000512015'}
    line_items = [item]

    response = create_sales_order(customer_id=customer_id, line_items=line_items)
    assert response is not None, "Response should not be None"
    assert isinstance(response, dict), "Response should be a dictionary"
    assert "sales_order" in response, "Response should contain 'sales_order' key"
    assert isinstance(response["sales_order"], dict), "'sales_order' should be a dictionary"
    assert "message" in response, "Response should contain 'message' key"
    assert isinstance(response["message"], str), "'message' should be a string"
    assert "created" in response["message"].lower(), "'message' should contain 'created'"

