"""The main entry point for this package."""
from typing import Dict

import docker

from .base import Base
from .configuration import ConfigurationManager


class Binocular(Base):
    """Named after the package and is consider the main entrypoint for this package.
    
    All commandline arguments will flow through this class. These will be defined as
    properties, methods and derived classes.
    """

    def __init__(self) -> None:
        """Main entry point, including pre-flight checks.
        
        We check to ensure Docker is installed before continuing.
        If it is not, we provide guidance and exit.
        """
        # First check for configuration file 
        Base.config_manager = ConfigurationManager()
        if not Base.config:
            self.get_config()
 
        # next we check for docker
        if not self._check_if_docker_is_installed():
            self.__logger.critical(
                "You must have Docker, Docker Desktop or some variant installed before continuing."
                "Before you can continue, you must have Docker installed. Visit https://docker.com"
                " for more information."
            )
        Base.docker_client = docker.from_env()
        self._build_image(name="builder", tag="binocular.builder")

        from .services.portalconfig import PortalConfig

        print(PortalConfig())

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

    def run(self, value: str) -> None:
        return_dict = {}
        iocs = self._get_ioc_type(value=value)
        config = self.get_config()
        for service in self.config["services"]:
            for key,val in self.config["services"][service].items():
                if key == "supported_indicators":
                    for ioc_type, ioc_val in iocs.items():
                        if ioc_type in val:
                            if ioc_val not in return_dict:
                                return_dict[ioc_val] = {}
                           # if service not in return_dict[ioc_val]:
                            #    return_dict[ioc_val][service] = 
                            return_dict[ioc_val].append()
          #      for 
        # for key, _val in config.items():
        #     if self.SERVICE_MAP.get(key):
        #         for k, v in iocs.items():
        #             if self.SERVICE_MAP[key].get(k):
        #                 if isinstance(v, list):
        #                     for item in v:
        #                         if item not in return_dict:
        #                             return_dict[item] = {}
        #                         if key not in return_dict[item]:
        #                             return_dict[item][key] = []
        #                         return_dict[item][key].append(self.SERVICE_MAP[key][k](item))
        # return return_dict

        for service in self.config.get("services"):
            if service == "virustotal":
                from .services.virustotal import VirusTotal

              #  response = VirusTotal(api_key=self.config["services"][service].get("api_key")).run(indicator=)

        from .services.virustotal import VirusTotal

        resp = VirusTotal().run()
        print(resp)
        pass
