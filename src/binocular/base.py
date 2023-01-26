"""binocular.base.

This Base class inherits from our LoggingBase metaclass and gives us
shared logging across any class inheriting from Base.
"""
import re
import os
import pathlib
import subprocess
from typing import AnyStr
from typing import Dict
from typing import List
from typing import Union

from .utils.logger import LoggingBase


class Base(metaclass=LoggingBase):
    """Base class to all other classes within this project."""

    BASE_IMAGE_FILE_PATH = pathlib.Path(__file__).parent.resolve() / "data/Dockerfile"
    docker_client = None
    base_image = None
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

    def _get_ioc_type(self, value: str) -> Dict[str, Union[str, List[str]]]:
        """Returns the determined IOC type from a given string.

        Args:
            value (str): The string to determine IOC type.

        Returns:
            Dict[str, Union[str, List[str]]]: _description_
        """
        return_dict: Dict[str, Union[str, List[str]]] = {}
        for key, val in self.PATTERNS.items():
            matches = re.findall(val, value)
            if matches:
                if key not in return_dict:
                    return_dict[key] = []
                return_dict[key].extend(matches)
        return return_dict

    def _get_absolute_path(self, path: str) -> AnyStr:
        """Extracts the absolute path from a given string path.

        Args:
            path (str): The path to get the absolute path from.

        Returns:
            AnyStr: The full absolute path of a value.
        """
        try:
            if pathlib.Path(path):
                return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))
        except Exception as e:
            self.__logger.critical(f"We are unable to determine the absolute path provided '{path}'. {e}")

    def _check_if_docker_is_installed(self) -> bool:
        """Checks whether or not Docker daemon is installed.

        Returns:
            bool: Returns true if docker is installed. False if not.
        """
        try:
            resp = subprocess.check_output("docker ps", shell=True)
            return True
        except subprocess.CalledProcessError as cpe:
            self.__logger.info(f"docker was not found. {cpe}")
            return False

    def _read_data_file(self, filename: str) -> str:
        """Will read a data file given it's name from the packages data directory.

        Args:
            filename (str): The filename of the file to read.

        Returns:
            str: The contents of that file are returned.
        """
        if pathlib.Path(f"{self.BASE_IMAGE_FILE_PATH}/data/{filename}").exists():
            with open(f"{self.BASE_IMAGE_FILE_PATH}/data/{filename}") as f:
                return f.read()
        else:
            self.__logger.critical(f"The provided filename '{filename}' does not exist!!")
            raise FileNotFoundError(f"The provided filename '{filename}' does not exist!!")

    def _build_image(self, name: str, tag: str) -> bool:
        """Builds a provided Docker image target name.

        Args:
            name (str): The target name of an image to build.
            tag (str): The tag to use for the image being built.

        Returns:
            bool: Whether or not the image built successfully or not.
        """
        try:
            self.__logger.info(f"Building container image '{name}' with tag '{tag}'")
            Base.base_image, build_logs = Base.docker_client.images.build(
                path=str(self.BASE_IMAGE_FILE_PATH.parent), 
                dockerfile=str(self.BASE_IMAGE_FILE_PATH.name),
                tag=tag,
                target=name,
            )
            return True
        except Exception as e:
            self.__logger.critical(f"Unable to build image '{name}'.")
            for item in build_logs:
                self.__logger.critical(item)
            return False
