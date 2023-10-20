import click

from arc.cli.utils import load_sdk, output_json, output_table
from arc.sdk.enums import AssetType


@click.group("assets")
def assets_group():
    """Asset management commands."""
    pass


@assets_group.command("get")
@click.argument("asset-id", type=click.UUID)
@click.option("--json", is_flag=True, help="Output result as json.")
def assets_get_command(asset_id: click.UUID, json: bool):
    """Get an asset by ID.

    ASSET-ID is the ID of the asset to get.
    """
    sdk = load_sdk()

    asset = sdk.get_asset(asset_id=str(asset_id))

    if asset is not None:
        output_table(values=[asset]) if not json else output_json([asset])


@assets_group.command("list")
@click.option("--json", is_flag=True, help="Output result as json.")
def get_all_assets(json: bool):
    """
    Get all assets.
    """
    sdk = load_sdk()

    assets = sdk.get_all_assets()

    output_table(values=assets) if not json else output_json(assets)


@assets_group.command("enable")
@click.argument("asset-id", type=click.UUID)
@click.option("--json", is_flag=True, help="Output result as json.")
def enable_asset_command(asset_id: click.UUID, json: bool):
    """Enable an asset in the tenant system.

    ASSET-ID is the ID of the asset to enable.
    """
    sdk = load_sdk()

    asset = sdk.enable_asset(asset_id=str(asset_id))

    output_table(values=[asset]) if not json else output_json([asset])


@assets_group.command("deploy-erc20")
@click.option("--name", type=str, prompt=True)
@click.option("--symbol", type=str, prompt=True)
@click.option("--quantum", type=int, prompt=False, default=1000000)
@click.option("--json", is_flag=True, help="Output result as json.")
def deploy_erc20_asset_command(name: str, symbol: str, quantum: int, json: bool):
    """Deploy a mintable ERC20 asset.

    NAME is the name of the asset.
    SYMBOL is the symbol of the asset.
    QUANTUM is the quantum of the asset.
    """
    sdk = load_sdk()

    asset = sdk.deploy_asset(AssetType.ERC20_MINTABLE, name=name, symbol=symbol, quantum=quantum)

    output_table(values=[asset]) if not json else output_json([asset])
