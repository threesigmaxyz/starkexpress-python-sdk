import keyring
from keyring.errors import PasswordDeleteError


NAMESPACE = "starkexpress-cli"
API_KEY_ENTRY = "API_KEY"


def get_credentials() -> str:
    api_key = keyring.get_password(NAMESPACE, API_KEY_ENTRY)

    return api_key


def is_logged_in() -> bool:
    return get_credentials() is not None


def login(api_key: str) -> None:
    keyring.set_password(NAMESPACE, API_KEY_ENTRY, api_key)


def logout() -> None:
    def safe_delete(entry: str) -> None:
        try:
            keyring.delete_password(NAMESPACE, entry)
        except PasswordDeleteError:
            pass

    safe_delete(API_KEY_ENTRY)
