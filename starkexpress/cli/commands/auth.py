import click

from starkexpress.cli.utils import output_json, output_table
from starkexpress.cli.utils.auth import get_credentials, is_logged_in, login, logout


@click.group("auth")
def auth_group():
    """Tenant authentication commands."""
    pass


@auth_group.command("login")
@click.option("--client-id", type=str, prompt=True)
@click.option("--client-secret", type=str, prompt=True)
@click.option("--json", is_flag=True, help="Output result as json.")
def login_command(client_id: str, client_secret: str, json: bool):
    """Login to StarkExpress."""
    # TODO validate credentials.
    login(client_id, client_secret)

    # TODO query tenant info.
    output = [{"clientId": client_id, "status": "CONNECTED"}]

    output_table(values=output) if not json else output_json(output)


@auth_group.command("status")
@click.option("--json", is_flag=True, help="Output result as json.")
def status_command(json: bool):
    """Display current authentication status."""
    logged_in = is_logged_in()

    status = "CONNECTED" if logged_in else "DISCONNECTED"
    output = [
        {"clientId": get_credentials()[0] if logged_in else "N/A", "status": status}
    ]

    output_table(values=output) if not json else output_json(output)


@auth_group.command("logout")
@click.option("--json", is_flag=True, help="Output result as json.")
def logout_command(json: bool):
    """Logout from StarkExpress."""
    logout()

    output = [{"clientId": "N/A", "status": "DISCONNECTED"}]

    output_table(values=output) if not json else output_json(output)
