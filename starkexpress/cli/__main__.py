import click

from starkexpress import __version__
from starkexpress.cli.commands import (
    assets_group,
    auth_group,
    deposits_group,
    fees_group,
    mints_group,
    transactions_group,
    transfers_group,
    users_group,
    utils_group,
    vaults_group,
    withdraws_group
)


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


@click.group()
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Show the current version and exit.",
)
def cli():
    """
    StarkExpress CLI

    The command line tool for StarkExpress.
    """
    pass


cli.add_command(auth_group)
cli.add_command(assets_group)
cli.add_command(deposits_group)
cli.add_command(fees_group)
cli.add_command(mints_group)
cli.add_command(transactions_group)
cli.add_command(transfers_group)
cli.add_command(users_group)
cli.add_command(utils_group)
cli.add_command(vaults_group)
cli.add_command(withdraws_group)

if __name__ == "__main__":
    # This is the entry point for the CLI.
    cli()
