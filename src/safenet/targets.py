""" Target module for safenet. """

import logging
from abc import ABC, abstractmethod

import requests

log = logging.getLogger(__name__)


class BaseTarget(ABC):
    """Base class for network targets."""

    @abstractmethod
    def check(self):
        """Check the target for network connectivity."""
        raise NotImplementedError


class WebsiteTarget(BaseTarget, ABC):
    """A target website."""

    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address


class UnsafeWebsite(WebsiteTarget):
    """An unsafe website that should not be available."""

    def __init__(self, name: str, address: str):
        super().__init__(name, address)
        self.logger = log.getChild("UnsafeWebsite")

    def check(self):
        """Verify HTTP connectivity is blocked to the website."""

        self.logger.debug("verify [%s] => %s", self.name, self.address)

        try:
            resp = requests.head(self.address)
            resp.raise_for_status()
        except requests.HTTPError:
            self.logger.info("[%s] is safe", self.name)
            return True

        self.logger.warning("[%s] is not safe", self.name)
        return False


class SafeWebsite(WebsiteTarget):
    """A safe website that should be available."""

    def __init__(self, name: str, address: str):
        super().__init__(name, address)
        self.logger = log.getChild("SafeWebsite")

    def check(self):
        """Verify HTTP connectivity is available to the website."""

        self.logger.debug("verify [%s] => %s", self.name, self.address)

        try:
            resp = requests.head(self.address)
            resp.raise_for_status()
        except requests.HTTPError:
            self.logger.warning("[%s] is not available", self.name)
            return False

        self.logger.info("[%s] is available", self.name)
        return True
