"""Application configuration data for safenet.

See the default config file for details on configuration options.
"""

import logging
import logging.config
import os
import os.path

import yaml
from pydantic import BaseModel, field_validator

from . import util
from .targets import (
    SafeNetworkTarget,
    SafePingTarget,
    SafeWebsite,
    UnsafeNetworkTarget,
    UnsafePingTarget,
    UnsafeWebsite,
)

log = logging.getLogger(__name__)


class WebTargetConfig(BaseModel):
    """Configuration for standard web targets."""

    name: str
    address: str
    safe: bool = False

    def initialize(self):
        """Initialize the web target for use."""
        log.info("initializing target: %s", self.name)

        if self.safe:
            return SafeWebsite(self.name, self.address)

        return UnsafeWebsite(self.name, self.address)


class PingTargetConfig(BaseModel):
    """Configuration for ping targets."""

    name: str
    address: str
    count: int = 3
    safe: bool = False

    def initialize(self):
        """Initialize the ping target for use."""
        log.info("initializing target: %s", self.name)

        if self.safe:
            return SafePingTarget(self.name, self.address, count=self.count)

        return UnsafePingTarget(self.name, self.address, count=self.count)


class NetworkTargetConfig(BaseModel):
    """Configuration for network targets."""

    name: str
    address: str
    port: int
    network: str = None
    safe: bool = False

    @field_validator("network")
    @classmethod
    def validate_network(cls, v, values):
        """Validate the network and determine the source IP if needed."""
        if v is None:
            return v

        source_ip = util.get_device_ip(v)

        if source_ip is None:
            raise ValueError(f"Unable to determine IP address for network: {v}")

        return source_ip

    def initialize(self):
        """Initialize the network target for use."""
        log.info("initializing target: %s", self.name)

        if self.safe:
            return SafeNetworkTarget(
                self.name,
                self.address,
                self.port,
                source_ip=self.network,
            )

        return UnsafeNetworkTarget(
            self.name,
            self.address,
            self.port,
            source_ip=self.network,
        )


class AppConfig(BaseModel):
    """Application configuration for safenet."""

    websites: list[WebTargetConfig] = []
    systems: list[PingTargetConfig] = []
    networks: list[NetworkTargetConfig] = []

    logging: dict | None = None

    @classmethod
    def load(cls, config_file):
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"config file does not exist: {config_file}")

        with open(config_file) as fp:
            data = yaml.load(fp, Loader=yaml.SafeLoader)
            conf = AppConfig(**data)

        logger = cls._configure_logging(conf)
        logger.debug("loaded AppConfig from: %s", config_file)

        return conf

    @classmethod
    def _configure_logging(cls, conf):
        if conf.logging is None:
            logging.basicConfig(level=logging.WARNING)
        else:
            logging.config.dictConfig(conf.logging)

        return logging.getLogger()
