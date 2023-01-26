"""VirusTotal service."""
import sys
from typing import Dict

from ..base import Base


class VirusTotal(Base):
    """The VirusTotal container service."""

    IMAGE_TARGET: str = "VTService"
    IMAGE_TAG: str = "binocular.virustotal"

    def __init__(self, api_key: str) -> None:
        """Main entry point where we build and define our service container.

        Args:
            api_key (str): The api_key to authenticate to VirusTotal.
        """
        self.image = self._build_image(name=self.IMAGE_TARGET, tag=self.IMAGE_TAG)
        self.api_key = api_key

    def run(self, indicator: str) -> Dict[str, str]:
        """Runs the created VirusTotal container and passes in parameters to authenticate and retrieve results from VT.

        Args:
            indicator (str): The indicator to lookup in VT.

        Returns:
            Dict[str, str]: The response from VT.
        """
        for item in Base.docker_client.images.list():
            for tag in item.tags:
                if self.IMAGE_TAG in tag:
                    self.__logger.info(f"Running container with tag of '{tag}'")
                    response = Base.docker_client.containers.run(item.id, f'python virustotal.py "{self.api_key}" "{indicator}"')
                    return response.decode('utf-8')


class VirusTotalService:

    def run(self, argv):
        import vt

        client = vt.Client(argv[0])

        url_id = vt.url_id(argv[1])
        url = client.get_object('/urls/{}', url_id)

        return_dict = {}
        for item in dir(url):
            if not item.startswith('_'):
                return_dict[item] = getattr(url, item)
        return return_dict


if __name__ == "__main__":
    print(VirusTotalService().run(sys.argv))
