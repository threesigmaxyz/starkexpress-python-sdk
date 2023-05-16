import click

from starkexpress.sdk.enums import DataAvailabilityMode, TransactionType
from starkexpress.cli.utils import load_sdk, output_json, output_table


@click.group("transfers")
def transfers_group():
    """Transfer operation commands."""
    pass


@transfers_group.command("list")
@click.option("--json", is_flag=True, help="Output result as json.")
def get_all_transfers_command(json: bool):
    """
    Get all transfer operations.
    """
    sdk = load_sdk()

    deposits = sdk.get_all_transactions(tx_type=TransactionType.Transfer)

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


@transfers_group.command("transfer")
@click.option(
    "--sender-id", type=click.UUID, required=True, help="The user ID of the sender."
)
@click.option(
    "--recipient-id",
    type=click.UUID,
    required=True,
    help="The user ID of the recipient.",
)
@click.option(
    "--asset-id",
    type=click.UUID,
    required=True,
    help="The ID of the asset to transfer.",
)
@click.option("--amount", type=int, required=True, help="The amount to transfer.")
@click.option(
    "--sender-da-mode",
    type=click.Choice(
        [DataAvailabilityMode.ZK_ROLLUP.name, DataAvailabilityMode.VALIDIUM.name]
    ),
    default=DataAvailabilityMode.ZK_ROLLUP.name,
    show_default=True,
    help="The sender data availability mode.",
)
@click.option(
    "--recipient-da-mode",
    type=click.Choice(
        [DataAvailabilityMode.ZK_ROLLUP.name, DataAvailabilityMode.VALIDIUM.name]
    ),
    default=DataAvailabilityMode.ZK_ROLLUP.name,
    show_default=True,
    help="The recipient data availability mode.",
)
@click.option(
    "--stark-private-key",
    type=str,
    prompt="STARK private key",
    help="The STARK private key of the sender.",
)  # TODO hide input
def transfer_command(
    sender_id: click.UUID,
    recipient_id: click.UUID,
    asset_id: click.UUID,
    amount: int,
    sender_da_mode: str,
    recipient_da_mode: str,
    stark_private_key: str,
    token_id: int = None,
):
    """Submit a transfer operation."""
    sdk = load_sdk()

    result = sdk.transfer(
        sender_id=str(sender_id),
        recipient_id=str(recipient_id),
        asset_id=str(asset_id),
        amount=amount,
        sender_da_mode=DataAvailabilityMode.__members__[sender_da_mode],
        recipient_da_mode=DataAvailabilityMode.__members__[recipient_da_mode],
        token_id=token_id,
        stark_private_key=stark_private_key,
    )

    if "errors" in result:
        output_json(values=result["errors"])
    else:
        filter_keys = [
            "userStarkKey",
            "vaultId",
            "availableBalance",
            "assetSymbol",
            "accountingBalance",
        ]
        result = [
            {key: value for key, value in vault.items() if key in filter_keys}
            for vault in result
        ]
        output_table(values=result)
