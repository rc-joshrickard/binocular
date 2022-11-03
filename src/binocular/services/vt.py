"""VirusTotal service integration."""
import vt

from ..base import Base


class VT(Base):
    """VirusTotal service class."""

    def __init__(self) -> None:
        """Used to connect to VirusTotal API via defined configuration and the vt-py client."""
        self.client = vt.Client(self.config.get("virustotal"))
        