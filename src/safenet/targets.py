""" Target module for safenet. """

import logging
import socket
from abc import ABC, abstractmethod

import ping3
import requests
from ping3.errors import PingError, Timeout

log = logging.getLogger(__name__)


class BaseTarget(ABC):
    """Base class for network targets."""

    @abstractmethod
    def check(self):
        """Check the target for network connectivity."""
        raise NotImplementedError


class SafeTargetMixin:
    """Mixin for targets that should be available.

    The target must define an `is_available` property for this mixin.
    """

    def check(self):
        """Verify connectivity is available to the target."""
        if self.is_available:
            self.logger.info("[%s] is available", self.name)
            return True

        self.logger.warning("[%s] is not available", self.name)
        return False


class UnsafeTargetMixin:
    """Mixin for targets that should not be available.

    The target must define an `is_available` property for this mixin.
    """

    def check(self):
        """Verify connectivity is blocked to the target."""
        if self.is_available:
            self.logger.warning("[%s] is not safe", self.name)
            return False

        self.logger.info("[%s] is safe", self.name)
        return True


class PingTarget(BaseTarget, ABC):
    """A target for pingable network addresses."""

    def __init__(
        self,
        name: str,
        address: str,
        timeout: int = 5,
        count: int = 1,
        ttl: int = 64,
        size: int = 56,
    ):
        self.name = name
        self.address = address
        self.count = count
        self.timeout = timeout
        self.ttl = ttl
        self.size = size

        self.logger = log.getChild("PingTarget")

    @property
    def is_available(self) -> bool:
        """Determine if the specified system is available."""

        self.logger.debug("ping [%s] => %s", self.name, self.address)

        # track the response times so we can average them later
        response_times = []

        for seq in range(0, self.count):
            try:
                delay = self.ping(seq)

                self.logger.debug("ping :: %s [%d] => %d sec", self.name, seq, delay)

                response_times.append(delay)

            except Timeout:
                self.logger.debug("ping timeout: %s", self.name)

            except PingError as err:
                self.logger.debug("ping error: %s => %s", self.name, err)

            except OSError as err:
                self.logger.debug("network error: %s => %s", self.name, err)

        if not response_times:
            return False

        avg_delay = sum(response_times) / len(response_times)
        self.logger.debug("[%s] is available : %f sec", self.name, avg_delay)

        return True

    def ping(self, seq=0):
        """Ping the configured target with a given sequence number."""

        self.logger.debug("ping :: %s @ %s [%d]", self.name, self.address, seq)

        delay = ping3.ping(
            self.address,
            timeout=self.timeout,
            ttl=self.ttl,
            size=self.size,
            seq=seq,
        )

        if delay is None:
            raise PingError("ping failed")

        return delay


class SafePingTarget(SafeTargetMixin, PingTarget):
    """A safe target that should be available."""

    def __init__(self, name: str, address: str, **kwargs):
        super().__init__(name, address, **kwargs)
        self.logger = log.getChild("SafePingTarget")


class UnsafePingTarget(UnsafeTargetMixin, PingTarget):
    """An unsafe target that should not be available."""

    def __init__(self, name: str, address: str, **kwargs):
        super().__init__(name, address, **kwargs)
        self.logger = log.getChild("UnsafePingTarget")


class WebsiteTarget(BaseTarget, ABC):
    """A target website."""

    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address

        self.logger = log.getChild("WebsiteTarget")

    @property
    def is_available(self) -> bool:
        """Determine if the specified website is available."""

        self.logger.debug("verify [%s] => %s", self.name, self.address)

        try:
            resp = requests.head(self.address, timeout=5)
            resp.raise_for_status()

            self.logger.debug("[%s] is available : %s", self.name, resp.status_code)

            return True

        except requests.RequestException as ex:
            self.logger.debug("RequestException: %s", ex)

        return False


class UnsafeWebsite(UnsafeTargetMixin, WebsiteTarget):
    """An unsafe website that should not be available."""

    def __init__(self, name: str, address: str):
        super().__init__(name, address)
        self.logger = log.getChild("UnsafeWebsite")


class SafeWebsite(SafeTargetMixin, WebsiteTarget):
    """A safe website that should be available."""

    def __init__(self, name: str, address: str):
        super().__init__(name, address)
        self.logger = log.getChild("SafeWebsite")


class NetworkTarget(BaseTarget, ABC):
    """A target for TCP/IP network connectivity checks."""

    def __init__(
        self,
        name: str,
        address: str,
        port: int,
        source_ip: str = None,
        timeout: int = 5,
    ):
        self.name = name
        self.address = address
        self.port = port
        self.source_ip = source_ip
        self.timeout = timeout

        self.logger = log.getChild("NetworkTarget")

    @property
    def is_available(self) -> bool:
        """Determine if the specified network service is available."""

        self.logger.debug(
            "connect [%s] => %s:%d from %s",
            self.name,
            self.address,
            self.port,
            self.source_ip or "<default>",
        )

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)

        if self.source_ip:
            sock.bind((self.source_ip, 0))

        try:
            sock.connect((self.address, self.port))
            self.logger.debug("[%s] connection successful", self.name)

            return True

        except socket.timeout:
            self.logger.debug("connection timeout: %s", self.name)

        except OSError as err:
            self.logger.debug("connection error: %s => %s", self.name, err)

        finally:
            sock.close()

        return False


class SafeNetworkTarget(SafeTargetMixin, NetworkTarget):
    """A safe network target that should be available."""

    def __init__(self, name: str, address: str, port: int, **kwargs):
        super().__init__(name, address, port, **kwargs)
        self.logger = log.getChild("SafeNetworkTarget")


class UnsafeNetworkTarget(UnsafeTargetMixin, NetworkTarget):
    """An unsafe network target that should not be available."""

    def __init__(self, name: str, address: str, port: int, **kwargs):
        super().__init__(name, address, port, **kwargs)
        self.logger = log.getChild("UnsafeNetworkTarget")
