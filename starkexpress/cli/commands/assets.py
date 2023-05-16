import click

from starkexpress.cli.utils import load_sdk, output_json, output_table


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
    sdk = load_sdk()

    assets = sdk.get_all_assets()

    output_table(values=assets) if not json else output_json(assets)


@assets_group.command("enable")
@click.argument("asset-id", type=click.UUID)
@click.option("--json", is_flag=True, help="Output result as json.")
def enable_asset_command(asset_id: click.UUID, json: bool):
    """Enable an asset by ID.

    ASSET-ID is the ID of the asset to enable.
    """
    sdk = load_sdk()

    asset = sdk.enable_asset(asset_id=str(asset_id))

    output_table(values=[asset]) if not json else output_json([asset])
