import click

from starkexpress.cli.utils import output_table
from starkexpress.sdk import StarkExpressSdk


@click.group("fees")
def fees_group():
    """Fee management commands."""
    pass


@fees_group.command("list")
def get_all_fees_command():
    """Get all fees."""
    sdk = StarkExpressSdk(
        client_id="Hbq4Q4ws0Lf8KqmyY9rD0nY1u2Aa7SYS",
        client_secret="P0oDqci1LyK3U7oZYLbQwNLlpEekNMoyrc-FYSqVWpAkkyjQ-B8w9dy38YHaGv7a",
        rpc_url="https://eth-goerli.g.alchemy.com/v2/n-8ZlU1-OeBOYCvjCZTQCPfs5dR_0Z75vvvvv",
    )

    result = sdk.get_all_fees()

    output_table(values=result)
