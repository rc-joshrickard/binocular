"""Main entrypoint for CLI and the rest of the project."""
from typing import Dict

from .base import Base
from .configuration import ConfigurationManager
from .services.vt import VT
from .services.urlscan import UrlScanIo


class Binocular(Base):
    """Main class and entry point for project."""

    def __init__(self) -> None:
        """Checks and determins if configuration file exists or not."""
        Base.config_manager = ConfigurationManager()
        if not Base.config:
            self.get_config()
        self.SERVICE_MAP = {
            "virustotal": {
                "url": VT().url,
                "md5": VT().md5,
                "sha1": VT().sha1,
                "sha256": VT().sha256
            },
            "urlscanio": {
                "url": UrlScanIo().url
            }
        }
        
    def get_config(self) -> Dict[str, str]:
        """Returns the current configuration file values.

        Returns:
            Dict[str, str]: Returns a dictionary of keys and values.
        """
        Base.config = Base.config_manager._read_from_disk(path=Base.config_manager.config_path)
        return Base.config

    def update_config(self) -> Dict[str, str]:
        """Returns the updated config, once updated.

        Returns:
            Dict[str, str]: Returns a dictionary of keys and values.
        """
        Base.config_manager._save_to_disk(path=Base.config_manager.config_path, data=Base.config_manager._prompt())
        return self.get_config()

    def magnify(self, value: str) -> Dict[str, str]:
        """Returns results from 1 or more threat intelligence providers.

        Returns:
            Dict[str, str]: _description_
        """
        return_dict = {}
        iocs = self._get_ioc_type(value=value)
        config = self.get_config()
        for key,val in config.items():
            if self.SERVICE_MAP.get(key):
                for k,v in iocs.items():
                    if self.SERVICE_MAP[key].get(k):
                        if isinstance(v, list):
                            for item in v:
                                if item not in return_dict:
                                    return_dict[item] = {}
                                if key not in return_dict[item]:
                                    return_dict[item][key] = []
                                return_dict[item][key].append(self.SERVICE_MAP[key][k](item))
        return return_dict
