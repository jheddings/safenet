""" Utility functions for safenet."""

import ipaddress
import logging

import click
import ifaddr

log = logging.getLogger(__name__)


def get_device_ip(cidr):
    log.debug("find device IP in network: %s", cidr or "<default>")
    network = ipaddress.ip_network(cidr, strict=False)

    # TODO maybe add support for the "default" IP (e.g. cidr=None)

    # check all available IP addresses on the machine
    for ip in get_all_ip_addresses():
        addr = ipaddress.ip_address(ip)
        log.debug(" -- check IP address: %s", addr)

        if addr in network:
            return ip

    return None


def get_all_ip_addresses():
    ip_addresses = []

    # find all available IP's from all adapters
    for adapter in ifaddr.get_adapters():
        for addr in adapter.ips:
            if addr.is_IPv4:
                ip_addresses.append(addr.ip)

    return ip_addresses


@click.group()
def main():
    """Test utility methods from the command line."""


@main.group("ip")
def cmd_ip():
    """IP address utilities."""


@cmd_ip.command("list")
def cmd_ip_list():
    """List all IP addresses on this device."""

    ips = get_all_ip_addresses()

    if ips:
        click.echo("Available IP addresses:")
        for ip in ips:
            click.echo(f"  - {ip}")
    else:
        click.echo("No IP addresses found", err=True)


@cmd_ip.command("find")
@click.argument("cidr", required=True)
def find_device_ip(cidr):
    """Find device IP in the specified network CIDR."""

    ip = get_device_ip(cidr)

    if ip:
        click.echo(f"Found device IP in network {cidr}: {ip}")
    else:
        click.echo(f"No IP address found in network {cidr}", err=True)


if __name__ == "__main__":
    main()
