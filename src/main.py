"""
Application to check public IP address and compare to CloudFlare's DNS.

TODO:
- [ ] Set CloudFlare DNS servers in the env file.
- [X] Set the domain in the env file.
- [ ] Spin out configurations into seperate file for local and systemd testing.
- [ ] Configure systemd service.
- [ ] Configure logging.
- [ ] Add error/change notifications.
- [X] Configure for nuitka.
- [ ] Configure github actions.

"""
import click
import os
from dotenv import load_dotenv
import dns.resolver
import requests

from config import __version__, __year__

load_dotenv()


def get_public_ip(domain: str = "https://api.ipify.org") -> str:
    """
    Get the public IP address of the network.

    Returns
    -------
    str
        The public IP address of the network.
    """
    address = ""
    try:
        address = requests.get(domain).text
        print(f"Public IP address: {address}")
    except Exception as e:
        print(f"Error: {e}")

    return address


def get_ip_address(domain: str, record_type: str = "A") -> str:
    """
    Get the IP address od the domain.

    Uses the Cloudflare DNS servers to check the public IP address of the origin
    server. The domain must not be proxied by Cloudflare.

    Parameters
    ----------
    domain : str
        The domain name.
    record_type : str, optional
        The record type. Default is "A".

    Returns
    -------
    str
        The IP address of the domain.
    """
    address = ""
    resolver = dns.resolver.Resolver()
    # TODO: Set these in the env file
    resolver.nameservers = ["1.1.1.1", "1.0.0.1"]

    try:
        answers = resolver.resolve(domain, record_type)
        for rdata in answers:
            address = rdata.address
            print(f"IP address for {domain}: {rdata.address}")
    except Exception as e:
        print(f"Error: {e}")

    return address


def ip_checker():
    """Check public IP against DNS IP."""
    # TODO: Move configs to config module.
    public_domain = os.getenv("PUBLIC_URL", "https://api.ipify.org")
    check_domain = os.getenv("CHECK_URL", "")

    public_ip = get_public_ip(public_domain)
    dns_ip = get_ip_address(check_domain)

    print(public_ip == dns_ip)


@click.command()
@click.option("-s", "--service", help="The URL to get the host public IP address.")
@click.option(
    "-d", "--domain", help="The domain to check the IP address against; example `google.com`."
)
@click.option(
    "-n", "--nameserver", multiple=True, help="The nameserver to use to resolve the IP addr."
)
@click.option("-V", "--version", is_flag=True, help="Print the version and exit.")
def main(
    service: str | None = None,
    domain: str | None = None,
    nameserver: tuple[str] | None = None,
    version: bool = False,
):
    """Application entry point.

    Parameters
    ----------
    service :
    domain :
    nameserver :
    version :
    """
    if version:
        print(f"IP-Checker v{__version__} ({__year__})")
        print("This is free software. There is NO warranty or liability by the authors.")
        return

    # TODO: Configuration settings here.

    ip_checker()


if __name__ == "__main__":
    main()
