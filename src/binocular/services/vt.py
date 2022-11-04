"""VirusTotal service integration."""
from typing import Dict

import vt

from ..base import Base


class VT(Base):
    """VirusTotal service class."""

    def __init__(self) -> None:
        """Used to connect to VirusTotal API via defined configuration and the vt-py client."""
        if self.config and self.config.get("virustotal"):
            self.client = vt.Client(self.config.get("virustotal"))

    def url(self, url: str) -> Dict[str, str]:
        """Searching URl on VirusTotal.

        Args:
            url (str): The url to search VT for.

        Returns:
            Dict[str, str]: The results from our search.
        """
        return_dict = {}
        url_id = vt.url_id(url)
        url = self.client.get_object("/urls/{}", url_id)
        for attribute in dir(url):
            if not attribute.startswith("_"):
                return_dict[attribute] = url.get(attribute)
        return return_dict

    def _request_file_lookup(self, lookup_value: str) -> Dict[str, str]:
        """Used by all methods in VT looking up hashes.

        Args:
            lookup_value (str): The lookup query value for get_object method call.

        Returns:
            Dict[str, str]: Response from VT.
        """
        return_dict = {}
        try:
            response = self.client.get_object(lookup_value)
            for attribute in dir(response):
                if not attribute.startswith("_"):
                    return_dict[attribute] = response.get(attribute)
        except vt.error.APIError as ve:
            self.__logger.info(f"Error occurred with VT: {ve}")
        return return_dict

    def md5(self, md5: str) -> Dict[str, str]:
        """Retrieves information about a given MD5 hash.

        Args:
            md5 (str): A MD5 hash.

        Returns:
            Dict[str, str]: Results from VirusTotal.
        """
        return self._request_file_lookup(f"/files/{md5}")

    def sha1(self, sha1: str) -> Dict[str, str]:
        """Retrieves information about a given SHA1 hash.

        Args:
            sha1 (str): A SHA1 hash.

        Returns:
            Dict[str, str]: Results from VirusTotal.
        """
        return self._request_file_lookup(f"/files/{sha1}")

    def sha256(self, sha256: str) -> Dict[str, str]:
        """Retrieves information about a given SHA256 hash.

        Args:
            sha256 (str): A SHA256 hash.

        Returns:
            Dict[str, str]: Results from VirusTotal.
        """
        return self._request_file_lookup(f"/files/{sha256}")
