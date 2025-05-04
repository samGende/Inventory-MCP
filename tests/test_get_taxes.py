import pytest 

from resources.taxes import get_taxes


def test_get_taxes():
    
    response = get_taxes(page=1, per_page=10)
    
    assert isinstance(response, dict)
    assert "page" in response
    assert "per_page" in response
    assert "has_more_page" in response
    assert "taxes" in response
    assert "message" in response
    assert isinstance(response["taxes"], list)
    assert len(response["taxes"]) <= 10
    assert all(isinstance(tax, dict) for tax in response["taxes"])
    assert all("tax_id" in tax for tax in response["taxes"])