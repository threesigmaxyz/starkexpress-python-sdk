import click

from arc.cli.utils import load_sdk, output_json, output_table


@click.group("vaults")
def vaults_group():
    """Vault management commands."""
    pass


@vaults_group.command("get")
@click.argument("vault-id", type=click.UUID)
@click.option("--json", is_flag=True, help="Output result as json.")
def get_vault_command(vault_id: click.UUID, json: bool):
    """Get a vault by ID.

    VAULT-ID is the ID of the vault to get.
    """
    sdk = load_sdk()

    vault = sdk.get_vault(vault_id=str(vault_id))

    if vault is not None:
        output_table(values=[vault]) if not json else output_json([vault])


@vaults_group.command("list")
@click.option("--json", is_flag=True, help="Output result as json.")
def get_all_vaults_command(json: bool):
    """
    Get all vaults.
    """
    sdk = load_sdk()

    vaults = sdk.get_all_vaults()

    output_table(values=vaults) if not json else output_json(vaults)
