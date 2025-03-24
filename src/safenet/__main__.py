"""Main entry point for pingdat."""

import logging

import click

from . import version
from .config import AppConfig

logger = logging.getLogger(__name__)


class MainApp:
    """Context used during main execution."""

    def __init__(self, config: AppConfig):
        self.logger = logger.getChild("MainApp")

        self.config = config

    def __call__(self):
        """Run the main application."""
        self.logger.info("starting scan")

        unsafe = 0

        for target in self.config.websites:
            self.logger.info("checking target: %s", target.name)

            web = target.initialize()

            if not web.check():
                unsafe += 1

        self.logger.info("scan complete")

        if unsafe > 0:
            raise SystemExit(unsafe)


@click.command()
@click.option(
    "--config",
    "-f",
    default="safenet.yaml",
    help="app config file (default: safenet.yaml)",
)
@click.version_option(
    version=version.__version__,
    package_name=version.__pkgname__,
    prog_name=version.__pkgname__,
)
def main(config):
    cfg = AppConfig.load(config)

    app = MainApp(cfg)

    app()


### MAIN ENTRY
if __name__ == "__main__":
    main()
