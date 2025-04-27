from utils.api import _save_token_to_cache, _load_token_from_cache, _get_access_token


def test_save_load_token_to_cache():
    test_token_date ={'access_toke': "test_access_token", 'expires_in': 3600}

    _save_token_to_cache(test_token_date)

    loaded_token_data = _load_token_from_cache()

    assert loaded_token_data == test_token_date, "Loaded token data does not match saved data" 

def test_get_access_token():
    access_token1 = _get_access_token()

    access_token2 = _get_access_token()

    assert access_token1 == access_token2, "Access tokens should be the same"
    assert access_token1 is not None, "Access token should not be None"

