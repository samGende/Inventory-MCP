import pytest 

from resources.composite_items import list_composite_items


def test_list_composite_test_items():
    search_text = "Cling"

    response = list_composite_items(page=1, per_page=10, search_text=search_text, sort_column="name")

    assert response is not None, "Response should not be None"
    assert isinstance(response, dict), "Response should be a dictionary"
    assert "composite_items" in response, "Response should contain 'composite_items' key"
    assert isinstance(response["composite_items"], list), "'composite_items' should be a list"
    assert len(response["composite_items"]) < 10, "'composite_items' list should be less than 10"

    if len(response["composite_items"]) > 0:
        for item in response["composite_items"]:
            assert isinstance(item, dict), "Each item should be a dictionary"
            assert "name" in item, "Each item should contain 'name' key"
            assert search_text.lower() in item["name"].lower(), f"Item name should contain '{search_text}'"