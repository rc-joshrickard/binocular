"""binocular.base.

This Base class inherits from our LoggingBase metaclass and gives us
shared logging across any class inheriting from Base.
"""
import os
import re
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union

from .utils.logger import LoggingBase


class Base(metaclass=LoggingBase):
    """Base class to all other classes within this project."""

    HEADERS = {"Content-Type": "application/json"}
    PATTERNS = {
        "url": "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)",
        "ipv4": r"^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
        "domain": "[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)",
        "sha256": r"\b[0-9a-f]{64}\b",
        "sha1": r"\b[0-9a-f]{40}\b",
        "md5": r"([a-fA-F\d]{32})",
    }
    config_manager = None
    config = None  # This is an empty variable that will contain our configuration values and thus inheritted by other classes for their use.

    def _get_absolute_path(self, path: str) -> str:
        try:
            if Path(path):
                return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))
        except Exception as e:
            self.__logger.critical(f"We are unable to determine the absolute path provided '{path}'. {e}")

    def _get_ioc_type(self, value: str) -> Dict[str, Union[str, List[str]]]:
        """Returns the determined IOC type from a given string.

        Args:
            value (str): The string to determine IOC type.

        Returns:
            Dict[str, Union[str, List[str]]]: _description_
        """
        return_dict = {}
        for key, val in self.PATTERNS.items():
            matches = re.findall(val, value)
            if matches:
                if key not in return_dict:
                    return_dict[key] = []
                return_dict[key].extend(matches)
        return return_dict
