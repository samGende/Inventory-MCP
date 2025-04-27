from resources.items import list_items


def test_list_items():

    response = list_items(page=1, per_page=10, search_text="K10", sort_column="name")

    print("Response from list_items:")

    assert isinstance(response, dict), "Response should be a dictionary"
    assert "items" in response, "Response should contain 'items' key"
    assert len(response["items"]) <= 10, "Response should contain at most 10 items"

    items = response.get("items", [])
    for item in items:
        assert "K10" in item.get("name"), "Item name should contain 'K10'"


