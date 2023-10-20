import click

from arc.cli.utils.auth import get_credentials, is_logged_in
from arc.cli.utils.output import output_json, output_table
from arc.sdk import ArcSdk


def load_sdk() -> ArcSdk:
    api_key = get_credentials()
    if not is_logged_in():
        click.echo("You need to log in first.")
        raise click.Abort()

    return ArcSdk(
        api_key=api_key,
        rpc_url="https://eth-goerli.g.alchemy.com/v2/n-8ZlU1-OeBOYCvjCZTQCPfs5dR_0Z75",
    )
