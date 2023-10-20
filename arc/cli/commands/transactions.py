import click

from arc.cli.utils import load_sdk, output_json, output_table
from arc.sdk.enums import DataAvailabilityMode


@click.group("transactions")
def transactions_group():
    """
    Transaction management commands.
    """
    pass


@transactions_group.command("get")
@click.argument("transaction-id", type=click.UUID)
def get_transaction_command(transaction_id: click.UUID):
    """Get a transaction by ID.

    TRANSACTION-ID is the ID of the transaction to get.
    """
    sdk = load_sdk()

    transaction = sdk.get_transaction(transaction_id=str(transaction_id))

    if transaction is not None:
        # Remove rawTransaction from the output.
        raw_transaction = transaction.pop("rawTransaction")
        output_table(values=[transaction])
        # TODO --details like flag output_table(values=[raw_transaction])


@transactions_group.command("list")
def get_all_transactions_command():
    """
    Get all transactions.
    """
    sdk = load_sdk()

    transactions = sdk.get_all_transactions()

    if len(transactions):
        # Remove rawTransaction from the output.
        output_table(
            values=list(
                map(
                    lambda d: {
                        key: value
                        for key, value in d.items()
                        if key != "rawTransaction"
                    },
                    transactions,
                )
            )
        )
