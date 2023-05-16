import click

from starkexpress.cli.utils import load_sdk, output_table


@click.group("fees")
def fees_group():
    """Fee management commands."""
    pass


@fees_group.command("list")
def get_all_fees_command():
    """Get all fees."""
    sdk = load_sdk()

    result = sdk.get_all_fees()

    output_table(values=result)
