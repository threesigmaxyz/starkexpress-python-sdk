import os
import click

from arc.sdk.enums import DataAvailabilityMode, TransactionType
from arc.cli.utils import load_sdk, output_json, output_table


@click.group("deposits")
def deposits_group():
    """Deposit operation commands."""
    pass


@deposits_group.command("list")
@click.option("--json", is_flag=True, help="Output result as json.")
def get_all_deposits_command(json: bool):
    """
    Get all deposit operations.
    """
    sdk = load_sdk()

    deposits = sdk.get_all_transactions(tx_type=TransactionType.Deposit)

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


@deposits_group.command("deposit")
@click.option(
    "--user-id", type=click.UUID, required=True, help="The user ID of the depositor."
)
@click.option(
    "--asset-id", type=click.UUID, required=True, help="The ID of the asset to deposit."
)
@click.option("--amount", type=int, required=True, help="The amount to deposit.")
@click.option("--token-id", required=False, help="The ID of the token to deposit.")
@click.option(
    "--da-mode",
    type=click.Choice(
        [DataAvailabilityMode.ZK_ROLLUP.name, DataAvailabilityMode.VALIDIUM.name]
    ),
    default=DataAvailabilityMode.ZK_ROLLUP.name,
    show_default=True,
    help="The data availability mode to use.",
)
@click.option(
    "--eth-private-key",
    type=str,
    prompt="Ethereum private key",
    default=lambda: os.environ.get("Arc_CLI_ETH_PRIVATE_KEY", ""),
    help="The Ethereum private key of the depositor.",
)  # TODO hide input
@click.option(
    "--wait-for-receipt",
    is_flag=True,
    help="Wait for the deposit tx to be included in a block.",
)
def deposit_command(
    user_id: click.UUID,
    asset_id: click.UUID,
    amount: int,
    da_mode: str,
    token_id: int,
    eth_private_key: str,
    wait_for_receipt: bool,
):
    """Submit a deposit operation."""
    sdk = load_sdk()

    result = sdk.deposit(
        user_id=str(user_id),
        asset_id=str(asset_id),
        amount=amount,
        da_mode=DataAvailabilityMode.__members__[da_mode],
        token_id=token_id,
        private_key=eth_private_key,
        wait_for_receipt=wait_for_receipt,
    )

    output_table(values=[result])
