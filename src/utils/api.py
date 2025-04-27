
import json 
import time 
import httpx

from utils.setting import settings


def _get_access_token():
    """Get the access token from the cache or refresh it if expired."""

    token_data = _load_token_from_cache()

    if token_data and "access_token" in token_data:
        # Check if the token is expired
        if time.time() < token_data["expires_at"]:
            return token_data["access_token"]

    # If the token is not in the cache or expired, refresh it
    
    refresh_token = settings.ZOHO_REFRESH_TOKEN
    client_id = settings.ZOHO_CLIENT_ID
    client_secret = settings.ZOHO_CLIENT_SECRET
    
    params = {
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
    }

    url = f"{settings.ZOHO_AUTH_BASE_URL}/token"


    try:
        response = httpx.post(url, params=params)
        response.raise_for_status()

        token_data = response.json()

        if "access_token" not in token_data:
            # Save the new token data to cache
            print("Access token not found in response")
            return None
        
        token_data = {
            "access_token": token_data["access_token"],
            "expires_at": time.time() + token_data["expires_in"],
        }
        _save_token_to_cache(token_data)
        return token_data["access_token"]
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return None




def _save_token_to_cache(token_data):
    """Save the token data to a cache file."""

    with open(settings.TOKEN_CACHE_FILE, "w") as f:
        json.dump(token_data, f)

def _load_token_from_cache():
    """Load the token data from a cache file."""
    try:
        with open(settings.TOKEN_CACHE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None