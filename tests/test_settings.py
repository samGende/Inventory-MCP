from utils.setting import settings


def test_settings():
    assert settings.ZOHO_CLIENT_ID is not None, "ZOHO_CLIENT_ID is not set"
    assert settings.ZOHO_CLIENT_SECRET is not None, "ZOHO_CLIENT_SECRET is not set"
    assert settings.ZOHO_REFRESH_TOKEN is not None, "ZOHO_REFRESH_TOKEN is not set"
    assert settings.ZOHO_ORGANIZATION_ID is not None, "ZOHO_ORGANIZATION_ID is not set"
    assert settings.ZOHO_API_BASE_URL is not None, "ZOHO_API_BASE_URL is not set"
    assert settings.ZOHO_AUTH_BASE_URL is not None, "ZOHO_AUTH_BASE_URL is not set"

def test_settings_as_dict():
    assert isinstance(settings.as_dict(), dict), "as_dict() should return a dictionary"

def test_settings_validate():
    try:
        assert settings.validate() == True, "Validation should pass"
    except ValueError as e:
        assert False, f"Validation failed: {str(e)}"