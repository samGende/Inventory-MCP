import pytest

from resources.contacts import list_contacts, get_contact


def test_list_contacts():
    contact_name = "Sam"
    response = list_contacts(page=1, per_page=10, query_params={"contact_name": contact_name})

    assert isinstance(response, dict), "Response should be a dictionary"
    assert "contacts" in response, "Response should contain 'items' key"
    assert len(response["contacts"]) <= 10, "Response should contain at most 10 items"

    contacts = response.get("items", [])
    for contact in contacts:
        assert contact_name in contact.get("contact_name"), f"Contact name should contain '{contact_name}'"


def test_get_contact():
    contact_name = "Sam"
    response = list_contacts(page=1, per_page=10, query_params={"contact_name": contact_name})
    assert isinstance(response, dict), "Response should be a dictionary"    
    assert "contacts" in response, "Response should contain 'items' key"
    assert len(response["contacts"]) > 0, "Response should contain at least one contact"

    contact = response.get("contacts", [])[0]
    contact_id = contact.get("contact_id")
    assert contact_id, "Contact ID should not be None"
    response = get_contact(contact_id)
    assert isinstance(response, dict), "Response should be a dictionary"
    assert "contact" in response, "Response should contain 'contact' key"
    assert response["contact"].get("contact_id") == contact_id, "Contact ID should match the requested contact"
    assert response["contact"].get("contact_name") == contact.get("contact_name"), "Contact name should match the requested contact"

