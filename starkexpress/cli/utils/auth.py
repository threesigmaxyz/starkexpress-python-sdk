import keyring
from keyring.errors import PasswordDeleteError


NAMESPACE = "starkexpress-cli"
CLIENT_ID_ENTRY = "CLIENT_ID"
CLIENT_SECRET_ENTRY = "CLIENT_SECRET"


def get_credentials() -> (str, str):
    client_id = keyring.get_password(NAMESPACE, CLIENT_ID_ENTRY)
    client_secret = keyring.get_password(NAMESPACE, CLIENT_SECRET_ENTRY)

    return client_id, client_secret


def is_logged_in() -> bool:
    client_id, client_secret = get_credentials()

    return client_id is not None and client_secret is not None


def login(client_id: str, client_secret: str) -> None:
    keyring.set_password(NAMESPACE, CLIENT_ID_ENTRY, client_id)
    keyring.set_password(NAMESPACE, CLIENT_SECRET_ENTRY, client_secret)


def logout() -> None:
    def safe_delete(entry: str) -> None:
        try:
            keyring.delete_password(NAMESPACE, entry)
        except PasswordDeleteError:
            pass

    safe_delete(CLIENT_ID_ENTRY)
    safe_delete(CLIENT_SECRET_ENTRY)
