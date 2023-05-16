import click

from starkexpress.sdk.enums import DataAvailabilityMode, TransactionType
from starkexpress.cli.utils import load_sdk, output_json, output_table


@click.group("withdraws")
def withdraws_group():
    """Withdraw operation commands."""
    pass


@withdraws_group.command("list")
@click.option("--json", is_flag=True, help="Output result as json.")
def get_all_withdraws_command(json: bool):
    """
    Get all withdraw operations.
    """
    sdk = load_sdk()

    deposits = sdk.get_all_transactions(tx_type=TransactionType.Withdrawal)

    if len(deposits):
        # Remove rawTransaction from the output.
        output = list(
                map(
                    lambda d: {
                        key: value
                        for key, value in d.items()
                        if key != "rawTransaction"
                    },
                    deposits,
                )
            )
        output_table(values=output) if not json else output_json(output)


@withdraws_group.command("withdraw")
@click.option(
    "--user-id", type=click.UUID, required=True, help="The user ID of the withdrawer."
)
@click.option(
    "--asset-id",
    type=click.UUID,
    required=True,
    help="The ID of the asset to withdraw.",
)
@click.option("--amount", type=int, required=True, help="The amount to withdraw.")
@click.option("--token-id", required=False, help="The ID of the token to withdraw.")
@click.option(
    "--da-mode",
    type=click.Choice(
        [DataAvailabilityMode.ZK_ROLLUP.name, DataAvailabilityMode.VALIDIUM.name]
    ),
    default=DataAvailabilityMode.ZK_ROLLUP.name,
    show_default=True,
    help="The data availability mode to use.",
)
def withdraw_command(
    user_id: click.UUID, asset_id: click.UUID, amount: int, token_id: int, da_mode: str
):
    """Submit a withdraw operation."""
    sdk = load_sdk()

    result = sdk.withdraw(
        user_id=str(user_id),
        asset_id=str(asset_id),
        amount=amount,
        da_mode=DataAvailabilityMode.__members__[da_mode],
        token_id=token_id,
    )

    if "errors" in result:
        output_table(values=result["errors"])
    else:
        output_table(values=[r["vault"] for r in result])
