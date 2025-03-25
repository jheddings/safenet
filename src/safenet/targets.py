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

    @property
    def is_available(self):
        """Determine if the current website is available."""

        self.logger.debug("verify [%s] => %s", self.name, self.address)

        try:
            resp = requests.head(self.address)
            resp.raise_for_status()
        except requests.RequestException as ex:
            self.logger.debug("RequestException: %s", ex)
            return False

        self.logger.debug("[%s] is available : %s", self.name, resp.status_code)

        return True


class UnsafeWebsite(WebsiteTarget):
    """An unsafe website that should not be available."""

    def __init__(self, name: str, address: str):
        super().__init__(name, address)
        self.logger = log.getChild("UnsafeWebsite")

    def check(self):
        """Verify HTTP connectivity is blocked to the website."""

        if self.is_available:
            self.logger.warning("[%s] is not safe", self.name)
            return False

        self.logger.info("[%s] is safe", self.name)
        return True


class SafeWebsite(WebsiteTarget):
    """A safe website that should be available."""

    def __init__(self, name: str, address: str):
        super().__init__(name, address)
        self.logger = log.getChild("SafeWebsite")

    def check(self):
        """Verify HTTP connectivity is available to the website."""

        if self.is_available:
            self.logger.info("[%s] is available", self.name)
            return True

        self.logger.warning("[%s] is not available", self.name)
        return False
