"""Configuration file."""
import json
import os
from string import Template
from typing import AnyStr
from typing import Dict
from typing import List

import yaml
from attrs import asdict
from attrs import define
from attrs import field
from attrs import fields
from prompt_toolkit import PromptSession

from .base import Base


@define
class ServiceConfiguration:
    """Inidividual service configuration options per indicator type."""

    name: AnyStr = field(factory=str)
    supported_indicators: List = field(factory=list)
    api_key: AnyStr = field(factory=str, metadata={"question": Template("Please provide your $servicename API key: ")})


@define
class InternalConfiguration:
    """Sets the internal configuration options for RC employees."""

    portal_key: AnyStr = field(factory=str)
    portal_cert_path: AnyStr = field(factory=str)
    portal_cert_key_path: AnyStr = field(factory=str)
    ca_cert_path: AnyStr = field(factory=str)
    excluded_customer_list: List = field(factory=list)


@define
class Configuration:
    """The main configuration data model."""

    services: List[ServiceConfiguration] = field(factory=list)
    internal: InternalConfiguration = field(factory=InternalConfiguration)

    def __attrs_post_init__(self):
        if self.services:
            return_list = []
            for item in self.services:
                return_list.append(ServiceConfiguration(**item))
            self.services = return_list

        if self.internal:
            self.internal = InternalConfiguration(**self.internal)


class ConfigurationManager(Base):
    """The main class used to manage retreiving and saving configuration files from disk."""

    CONFIG_PATH = "~/.config/binocular.yml"
    session = PromptSession()

    def __init__(self) -> None:
        """Determines if configuration file exists or not."""
        self.config_path = self._get_absolute_path(path=self.CONFIG_PATH)
        if not os.path.exists(self.config_path):
            self._save_to_disk(path=self.config_path, data=self._prompt())

    def _prompt(self) -> Dict[str, str]:
        """Prompts the user to enter values for the defined services in our Configuration data model.

        The questions are metadata within our Configuration data model using string Templates.

        Returns:
            Dict[str, str]: A dictionary of the provided answers to our configuration questions.
        """
        return_list = []

        return asdict(
            Configuration(
                virustotal=self.session.prompt(fields(Configuration).virustotal.metadata["question"].substitute()),
                urlscanio=self.session.prompt(fields(Configuration).urlscanio.metadata["question"].substitute()),
            )
        )

    def _read_from_disk(self, path: str) -> Dict[str, str]:
        """Retreives the configuration file values from a given path on the disk.

        Args:
            path (str): The path to the configuration file on disk.

        Raises:
            FileNotFoundError: Raises when the file cannot be found.
            IsADirectoryError: Raises when the provided path is a directory.

        Returns:
            Dict[str, str]: A dictionary containing the defined services keys and values.
        """
        if os.path.exists(path) and os.path.isfile(path):
            try:
                with open(path) as f:
                    if path.endswith(".json"):
                        return json.load(f)
                    elif path.endswith(".yml") or path.endswith(".yaml"):
                        return yaml.load(f, Loader=yaml.SafeLoader)
                    else:
                        raise FileNotFoundError(f"The provided path value '{path}' is not one of '.yml'.")
            except Exception as e:
                self.__logger.warning(f"The provided config file {path} is not in the correct format. {e}")
        elif os.path.isdir(path):
            raise IsADirectoryError(f"The provided path is a directory and must be a file: {path}")

    def _save_to_disk(self, path: str, data: Dict[str, str]) -> None:
        """Saves the provided configuration data to the provided path.

        Args:
            path (str): The path to save our configuration data.
            data (Dict[str, str]): The data to save within our configuration file.

        Raises:
            Exception: Raises when an unknown exception is made.
            FileNotFoundError: Raises when the file cannot be found.
            IsADirectoryError: Raises when the provided value is a directory.
        """
        try:
            if not os.path.exists(os.path.dirname(path)):
                try:
                    os.makedirs(os.path.dirname(path))
                except Exception as e:
                    message = f"Attempted to create the provided directories '{path}' but was unable to."
                    self.__logger.critical(message + e)
                    raise e
            with open(path, "w+") as f:
                if path.endswith(".json"):
                    json.dump(data, f)
                elif path.endswith(".yml") or path.endswith(".yaml"):
                    yaml.dump(data, f)
                else:
                    raise FileNotFoundError(f"The provided path value '{path}' is not one of '.yml'.")
        except IsADirectoryError as ie:
            raise ie
