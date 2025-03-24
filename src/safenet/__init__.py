"""Module interface to safenet."""

import logging

import requests

log = logging.getLogger(__name__)


class WebTarget:
    """A target host for network operations."""

    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address

        self.log = log.getChild("WebTarget")

    def is_safe(self):
        """Verify HTTP connectivity is blocked to the web target."""

        self.log.debug("verify [%s] => %s", self.name, self.address)

        try:
            resp = requests.head(self.address)
            resp.raise_for_status()
        except requests.RequestException:
            self.log.info("[%s] marked as safe", self.name)
            return True

        self.log.warning("[%s] is not safe", self.name)

        return False
