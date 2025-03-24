""" Target module for safenet. """

import logging

import requests

log = logging.getLogger(__name__)

# TODO add support for known "safe" websites (verify they are reachable)


class WebTarget:
    """A target host for network operations."""

    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address

        self.log = log.getChild("WebTarget")

    def check(self):
        """Verify HTTP connectivity is blocked to the web target."""

        self.log.debug("verify [%s] => %s", self.name, self.address)

        resp = requests.head(self.address)

        if resp.ok:
            self.log.warning("[%s] is not safe", self.name)
            return False

        self.log.info("[%s] marked as safe", self.name)
        return True
