"""Main entrypoint for CLI and the rest of the project."""
from typing import Dict

from .base import Base
from .configuration import ConfigurationManager


class Binocular(Base):
    """Main class and entry point for project."""

    def __init__(self) -> None:
        """Checks and determins if configuration file exists or not."""
        self.config = ConfigurationManager()

    def get_config(self) -> Dict[str, str]:
        """Returns the current configuration file values.

        Returns:
            Dict[str, str]: Returns a dictionary of keys and values.
        """
        return self.config._read_from_disk(path=self.config.config_path)

    def update_config(self) -> Dict[str, str]:
        """Returns the updated config, once updated.

        Returns:
            Dict[str, str]: Returns a dictionary of keys and values.
        """
        self.config._save_to_disk(path=self.config.config_path, data=self.config._prompt())
        return self.get_config()

    def magnify(self, value: str) -> Dict[str, str]:
        """Returns results from 1 or more threat intelligence providers.

        Returns:
            Dict[str, str]: _description_
        """
        # Please note that I have not implemented the services components yet.
        iocs = self._get_ioc_type(value=value)
        return iocs
