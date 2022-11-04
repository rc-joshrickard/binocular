"""urlscanio service integration."""
from typing import Dict

import requests

from ..base import Base


class UrlScanIo(Base):
    """urlscan.io service class."""

    URL = "https://urlscan.io/api/v1"
    HEADERS = {"Content-Type": "application/json", "API-Key": None}

    def __init__(self) -> None:
        """Used to connect to urlscan.io API via defined configuration and the urlscanio client."""
        self.HEADERS["API-Key"] = self.config.get("urlscanio")

    def url(self, url: str) -> Dict[str, str]:
        """Search for the provided URl on urlscan.io.

        Args:
            url (str): The url to search for.

        Returns:
            Dict[str, str]: The results from the search.
        """
        response = requests.get(f"{self.URL}/search/?q={url}")
        if response and response.ok:
            return response.json()
