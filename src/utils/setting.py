import os
from typing import Dict, Any
from dotenv import load_dotenv

config_path = os.path.join(os.path.dirname(__file__), "../../config")
env_path = config_path +  "/.env"


token_cache_path = config_path + "/token_cach.json"


if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    print(".env file not found, loading default environment variables")
    load_dotenv()


class Settings:
    # API Credentials
    ZOHO_CLIENT_ID:str = os.getenv("ZOHO_CLIENT_ID")
    ZOHO_CLIENT_SECRET:str = os.getenv("ZOHO_CLIENT_SECRET")
    ZOHO_REFRESH_TOKEN:str = os.getenv("ZOHO_REFRESH_TOKEN")
    ZOHO_ORGANIZATION_ID:str = os.getenv("ZOHO_ORGANIZATION_ID")

    # ZOHO API URLs
    ZOHO_API_BASE_URL = os.getenv(
        "ZOHO_API_BASE_URL", "https://www.zohoapis.com/inventory/v1"
    )
    ZOHO_AUTH_BASE_URL = os.getenv(
        "ZOHO_AUTH_BASE_URL", f"https://accounts.zoho.com/oauth/v2"
    )

    TOKEN_CACHE_FILE = token_cache_path

    def as_dict(self) -> Dict[str, Any]:
        """Return settings as a dictionary."""
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_") and key.isupper()
        }

    def validate(self):
        "validate that the required settings are included"

        required_settings = [
            "ZOHO_CLIENT_ID",
            "ZOHO_CLIENT_SECRET",
            "ZOHO_REFRESH_TOKEN",
            "ZOHO_ORGANIZATION_ID",
        ]

        missing_settings = [
            setting for setting in required_settings if not getattr(self, setting)
        ]

        if missing_settings:
            raise ValueError(
                f"Missing required settings: {', '.join(missing_settings)}"
            )
        return True


settings = Settings()
