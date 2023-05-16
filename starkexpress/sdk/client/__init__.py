import requests

from typing import Any, Dict, List, Tuple

from starkexpress.sdk.enums import DataAvailabilityMode
from starkexpress.sdk.exceptions import StarkExpressApiException


STARKEXPRESS_API_ENDPOINT = "https://testnet-api.starkexpress.io"
STARKEXPRESS_OAUTH_ENDPOINT = "https://starkexpress-testnet.eu.auth0.com"
STARKEXPRESS_OAUTH_AUDIENCE = "https://testnet-api.starkexpress.io/"


class StarkExpressClient(object):
    """
    StarkExpress API client.

    This will be replaced with an auto-generated client from the following OpenAPI spec:
    https://starkexpress.redoc.ly/7f5cc840-50cd-43a4-aab2-49274c4704af
    """

    DEFAULT_PAGE_SIZE = 100

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def __auth(self) -> str:
        endpoint = f"{STARKEXPRESS_OAUTH_ENDPOINT}/oauth/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": STARKEXPRESS_OAUTH_AUDIENCE,
        }

        response = requests.post(endpoint, json=data)
        if response.status_code != 200:
            raise StarkExpressApiException(response.text)

        return response.json()["access_token"]

    def __get(self, path: str, params: Dict[str, Any] = None):
        endpoint = f"{STARKEXPRESS_API_ENDPOINT}{path}"
        headers = {
            "Authorization": "Bearer " + self.__auth(),  # TODO cache this
            "Content-Type": "application/json",
        }
        response = requests.get(endpoint, params=params, headers=headers)
        if response.status_code != 200:
            raise StarkExpressApiException(response.text)
        return response.json()

    def __post(self, path: str, body: Dict[str, Any] = None):
        endpoint = f"{STARKEXPRESS_API_ENDPOINT}{path}"
        headers = {
            "Authorization": "Bearer " + self.__auth(),  # TODO cache this
            "Content-Type": "application/json",
        }
        response = requests.post(endpoint, json=body, headers=headers)
        if response.status_code not in [200, 201]:
            raise StarkExpressApiException(response.text)
        return response.json()

    def get_user(self, user_id: str) -> Dict[str, Any]:
        return self.__get(f"/api/v1/users/{user_id}")

    def get_users(
        self, page_size: int = DEFAULT_PAGE_SIZE, page_number: int = 1
    ) -> List[Dict[str, Any]]:
        params = {"page_size": page_size, "page_number": page_number}
        return self.__get("/api/v1/users", params=params)["data"]

    def get_register_details(
        self, username: str, eth_address: str, stark_key: str
    ) -> Dict[str, Any]:
        params = {"username": username, "address": eth_address, "stark_key": stark_key}
        # TODO in updated details with standard eip712 format an signable hash ["typedData"]
        return self.__get("/api/v1/users/register-details", params=params)

    def register_user(
        self,
        username: str,
        eth_address: str,
        stark_public_key: str,
        eip712_signature: str,
        stark_signature: Tuple[str, str],
    ) -> Dict[str, Any]:
        body = {
            "username": username,
            "address": eth_address,
            "starkKey": stark_public_key,
            "eip712Signature": eip712_signature,
            "starkSignature": {
                "r": stark_signature[0],
                "s": stark_signature[1],
            },
        }
        return self.__post("/api/v1/users", body=body)

    def get_asset(self, asset_id: str) -> Dict[str, Any]:
        return self.__get(f"/api/v1/assets/{asset_id}")

    def get_assets(
        self, page_size: int = DEFAULT_PAGE_SIZE, page_number: int = 1
    ) -> List[Dict[str, Any]]:
        params = {"page_size": page_size, "page_number": page_number}
        return self.__get(f"/api/v1/assets", params=params)["data"]

    def enable_asset(self, asset_id: str) -> Dict[str, Any]:
        body = {"assetId": asset_id}
        return self.__post("/api/v1/assets", body=body)

    def get_vault(self, vault_id: str) -> Dict[str, Any]:
        return self.__get(f"/api/v1/vaults/{vault_id}")

    def get_vaults(
        self, page_size: int = DEFAULT_PAGE_SIZE, page_number: int = 1
    ) -> List[Dict[str, Any]]:
        params = {"page_size": page_size, "page_number": page_number}
        return self.__get("/api/v1/vaults", params=params)["data"]

    def get_fees(
        self, page_size: int = DEFAULT_PAGE_SIZE, page_number: int = 1
    ) -> List[Dict[str, Any]]:
        params = {"page_size": page_size, "page_number": page_number}
        return self.__get("/api/v1/fees", params=params)["data"]

    def get_transaction(self, transaction_id: str) -> Dict[str, Any]:
        return self.__get(f"/api/v1/transactions/{transaction_id}")

    def get_transactions(
        self,
        tx_type: str = None,
        page_size: int = DEFAULT_PAGE_SIZE,
        page_number: int = 1,
    ) -> List[Dict[str, Any]]:
        params = {"page_size": page_size, "page_number": page_number}
        params.update(
            {"tx_type": tx_type, "tx_type_comparison": "IsEqualTo"} if tx_type else {}
        )
        return self.__get("/api/v1/transactions", params=params)["data"]

    def get_deposit_details(
        self,
        user_id: str,
        asset_id: str,
        amount: str,
        da_mode: DataAvailabilityMode,
        token_id: int = None,
    ) -> Dict[str, Any]:
        # TODO token ID
        body = {
            "userId": user_id,
            "assetId": asset_id,
            "amount": str(amount),
            "dataAvailabilityMode": da_mode.value,
        }
        return self.__post("/api/v1/vaults/deposit-details", body=body)

    def get_transfer_details(
        self,
        sender_id: str,
        receiver_id: str,
        asset_id: str,
        amount: str,
        sender_da_mode: DataAvailabilityMode,
        receiver_da_mode: DataAvailabilityMode,
        token_id: int = None,
    ) -> Dict[str, Any]:
        # TODO token ID
        body = {
            "senderUserId": sender_id,
            "receiverUserId": receiver_id,
            "assetId": asset_id,
            "amount": str(amount),
            "senderDataAvailabilityMode": sender_da_mode.value,
            "receiverDataAvailabilityMode": receiver_da_mode.value,
        }
        return self.__post("/api/v1/transfers/details", body=body)

    def transfer(
        self,
        sender_vault_id: str,
        receiver_vault_id: str,
        quantized_amount: str,
        expiration_timestamp: int,
        nonce: int,
        stark_signature: Tuple[str, str],
    ):
        body = {
            "senderVaultId": sender_vault_id,
            "receiverVaultId": receiver_vault_id,
            "quantizedAmount": quantized_amount,
            "expirationTimestamp": expiration_timestamp,
            "nonce": nonce,
            "signature": {
                "r": stark_signature[0],
                "s": stark_signature[1],
            },
        }
        return self.__post("/api/v1/transfers", body=body)

    def mint(self, users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        body = {"users": users}
        return self.__post("/api/v1/mint", body=body)

    def withdraw(self, vault_id: str, amount: str) -> List[Dict[str, Any]]:
        body = {
            "vaultId": vault_id,
            "amount": amount,
        }
        return self.__post("/api/v1/vaults/withdraw", body=body)
