import click

from starkexpress.sdk.crypto.eth import (
    generate_eth_keys,
    get_eth_address_from_private_key,
)

from starkexpress.sdk.crypto.stark import (
    generate_stark_keys,
)

from starkexpress.cli.utils import (
    output_json,
    output_table,
)


@click.group("utils")
def utils_group():
    """General utility commands."""
    pass


@utils_group.command("gen-eth-keys")
@click.option(
    "--count", default=1, show_default=True, help="Number of key pairs to generate."
)
@click.option("--json", is_flag=True, help="Output result as json.")
def generate_eth_keys_command(count: int, json: bool):
    """Generate an Ethereum key pair."""
    private_keys = [generate_eth_keys()[0] for _ in range(count)]
    addresses = [get_eth_address_from_private_key(key) for key in private_keys]

    output = [
        {
            "Address": address,
            "PrivateKey": private_key,
        }
        for address, private_key in zip(addresses, private_keys)
    ]

    output_table(values=output) if not json else output_json(output)


@utils_group.command("gen-stark-keys")
@click.option(
    "--count", default=1, show_default=True, help="Number of key pairs to generate."
)
@click.option("--json", is_flag=True, help="Output result as json.")
def generate_stark_keys_command(count: int, json: bool):
    """Generate a STARK key pair."""
    keys = [generate_stark_keys() for _ in range(count)]

    output = [
        {
            "PublicKey": public_key,
            "PrivateKey": private_key,
        }
        for public_key, private_key in keys
    ]

    output_table(values=output) if not json else output_json(output)
