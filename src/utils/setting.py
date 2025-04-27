import os
from typing import Dict, Any
from dotenv import load_dotenv


env_path = os.path.join(os.path.dirname(__file__), "../config/.env")

if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    print(".env file not found, loading default environment variables")
    load_dotenv()


class Settings:
    # API Credentials
    ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
    ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
    ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
    ZOHO_ORGANIZATION_ID = os.getenv("ZOHO_ORGANIZATION_ID")

    # ZOHO API URLs
    ZOHO_API_BASE_URL = os.getenv(
        "ZOHO_API_BASE_URL", "https://www.zohoapis.com/inventory/v1"
    )
    domain = os.getenv("ZOHO_REGION", "US")
    ZOHO_AUTH_BASE_URL = os.getenv(
        "ZOHO_AUTH_BASE_URL", f"https://accounts.zoho.{domain}.com/oauth/v2"
    )

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
