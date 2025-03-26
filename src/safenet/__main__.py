"""Main entry point for pingdat."""

import logging

import click

from . import version
from .config import AppConfig

log = logging.getLogger(__name__)


class MainApp:
    """Context used during main execution."""

    def __init__(self, config: AppConfig):
        self.config = config
        self.logger = log.getChild("MainApp")

    def __call__(self):
        """Run the main application."""
        self.logger.info("starting scan")

        failed = 0

        self.logger.info("checking websites")
        for target in self.config.websites:
            self.logger.debug("checking target: %s", target.name)

            web = target.initialize()

            if not web.check():
                failed += 1

        self.logger.info("checking systems")
        for target in self.config.systems:
            self.logger.debug("checking target: %s", target.name)

            ping = target.initialize()

            if not ping.check():
                failed += 1

        self.logger.info("scan complete")

        if failed > 0:
            raise SystemExit(failed)


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
