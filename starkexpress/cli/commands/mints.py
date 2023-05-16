import click

from starkexpress.cli.utils import load_sdk, output_json, output_table
from starkexpress.sdk.enums import DataAvailabilityMode, TransactionType


@click.group("mints")
def mints_group():
    """Mint operation commands."""
    pass


@mints_group.command("list")
@click.option("--json", is_flag=True, help="Output result as json.")
def get_all_mints_command(json: bool):
    """
    Get all mint operations.
    """
    sdk = load_sdk()

    deposits = sdk.get_all_transactions(tx_type=TransactionType.Mint)

    if len(deposits):
        # Remove rawTransaction from the output.
        output = list(
            map(
                lambda d: {
                    key: value for key, value in d.items() if key != "rawTransaction"
                },
                deposits,
            )
        )
        output_table(values=output) if not json else output_json(output)


@mints_group.command("mint")
@click.option(
    "--user-id", type=click.UUID, required=True, help="The user ID of the recipient."
)
@click.option(
    "--asset-id",
    type=click.UUID,
    required=True,
    help="The ID of the asset to transfer.",
)
@click.option("--amount", type=int, required=True, help="The amount to transfer.")
@click.option(
    "--da-mode",
    type=click.Choice(
        [DataAvailabilityMode.ZK_ROLLUP.name, DataAvailabilityMode.VALIDIUM.name]
    ),
    default=DataAvailabilityMode.ZK_ROLLUP.name,
    show_default=True,
    help="The sender data availability mode.",
)
@click.option(
    "--token-id", type=int, required=False, help="The ID of the token to mint."
)
@click.option("--json", is_flag=True, help="Output result as json.")
def mint_command(
    user_id: click.UUID,
    asset_id: click.UUID,
    amount: int,
    da_mode: str,
    json: bool,
    token_id: int = None,
):
    """Submit a mint operation."""
    sdk = load_sdk()

    result = sdk.mint(
        user_id=str(user_id),
        asset_id=str(asset_id),
        amount=amount,
        da_mode=DataAvailabilityMode.__members__[da_mode],
        token_id=token_id,
    )

    # TODO bad format indexed by user id
    if "errors" in result:
        output_table(values=result["errors"])
    else:
        output_table(values=result) if not json else output_json(result)
