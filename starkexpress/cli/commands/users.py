import click

from starkexpress.cli.utils import load_sdk, output_json, output_table
from starkexpress.sdk.crypto.eth import generate_eth_keys
from starkexpress.sdk.crypto.stark import generate_stark_keys


@click.group("users")
def users_group():
    """User management commands."""
    pass


@users_group.command("get")
@click.argument("user-id", type=click.UUID)
@click.option("--json", is_flag=True, help="Output result as json.")
def users_get_command(user_id: click.UUID, json: bool):
    """Get a user by ID.

    USER-ID is the ID of the user to get.
    """
    sdk = load_sdk()

    user = sdk.get_user(user_id=str(user_id))

    if json:
        output_json(values=[user])
    else:
        output_table(values=[user["user"]])
        output_json(
            values=[
                vault for vaults in user["vaultsPerAsset"].values() for vault in vaults
            ]
        )


@users_group.command("list")
@click.option("--json", is_flag=True, help="Output result as json.")
def users_command(json: bool):
    """
    Get all users.
    """
    sdk = load_sdk()

    users = sdk.get_all_users()

    output_table(values=users) if not json else output_json(users)


@users_group.command("register")
@click.argument("username", type=str)
@click.option(
    "--eth-key", default=generate_eth_keys()[0], help="Your Ethereum private key"
)
@click.option(
    "--stark-key", default=generate_stark_keys()[0], help="Your STARK private key"
)
@click.option("--json", is_flag=True, help="Output result as json.")
def register_command(username: str, eth_key: str, stark_key: str, json: bool):
    """Register a user.

    USERNAME is the username of the user to register.
    """
    sdk = load_sdk()

    user = sdk.register_user(username, eth_key, stark_key)

    output_table(values=[user]) if not json else output_json([user])
