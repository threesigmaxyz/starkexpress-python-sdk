import click

from starkexpress.cli.utils.auth import get_credentials, is_logged_in
from starkexpress.cli.utils.output import output_json, output_table
from starkexpress.sdk import StarkExpressSdk


def load_sdk() -> StarkExpressSdk:
    client_id, client_secret = get_credentials()
    if not is_logged_in():
        click.echo("You need to log in first.")
        raise click.Abort()

    return StarkExpressSdk(
        client_id=client_id,
        client_secret=client_secret,
        rpc_url="https://eth-goerli.g.alchemy.com/v2/n-8ZlU1-OeBOYCvjCZTQCPfs5dR_0Z75",
    )
