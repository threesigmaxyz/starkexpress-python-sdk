import json
import os

from typing import Any, Dict, List

from web3 import Web3

from starkexpress.sdk.client import StarkExpressClient
from starkexpress.sdk.crypto.eth import (
    get_eth_address_from_private_key,
    sign_eip712_register_message,
)
from starkexpress.sdk.crypto.stark import (
    get_stark_public_key_from_private_key,
    sign_message,
    get_transfer_msg,
    pedersen_hash,
)
from starkexpress.sdk.enums import (
    DataAvailabilityMode,
    TransactionType,
)


STARkEX_ABI_FILENAME = os.path.join(
    os.path.dirname(__file__), "starkex_v45.json"
)
STARkEX_ABI = json.load(open(STARkEX_ABI_FILENAME))


class StarkExpressSdk(object):
    def __init__(self, client_id: str, client_secret: str, rpc_url: str):
        self._client = StarkExpressClient(client_id, client_secret)

        self._web3 = Web3(Web3.HTTPProvider(rpc_url))
        # TODO assert self._web3.is_connected()

        self._starkEx = self._web3.eth.contract(
            address=self._web3.to_checksum_address(
                "0x999458e70e1422d3b5d9f277da5a7435224ed9c1"
            ),
            abi=STARkEX_ABI,
        )

    def get_user(self, user_id: str) -> Dict[str, Any]:
        return self._client.get_user(user_id)

    def get_all_users(self) -> List[Dict[str, Any]]:
        return self._client.get_users()

    def register_user(
        self, username: str, eth_private_key: str, stark_private_key: str
    ) -> Dict[str, Any]:
        # Compute public keys.
        eth_address = get_eth_address_from_private_key(eth_private_key)
        stark_public_key = get_stark_public_key_from_private_key(stark_private_key)

        # Query the StarkExpress API for the registration details.
        register_details = self._client.get_register_details(
            username=username, eth_address=eth_address, stark_key=stark_public_key
        )

        # Sign the EI712 registration message.
        # TODO encode body in other way, this makes it useless to call the API since the payload format is known.
        eip712_signature = sign_eip712_register_message(
            register_details, eth_private_key
        )

        # Sign the Ethereum address.
        stark_signature = sign_message(pedersen_hash(eth_address), stark_private_key)

        # Send the registration request to the StarkExpress API.
        return self._client.register_user(
            username=username,
            eth_address=eth_address,
            stark_public_key=stark_public_key,
            eip712_signature=eip712_signature,
            stark_signature=stark_signature,
        )

    def get_asset(self, asset_id: str) -> Dict[str, Any]:
        return self._client.get_asset(asset_id)

    def get_all_assets(self) -> List[Dict[str, Any]]:
        return self._client.get_assets()

    def enable_asset(self, asset_id: str) -> Dict[str, Any]:
        return self._client.enable_asset(asset_id)

    def get_vault(self, vault_id: str) -> Dict[str, Any]:
        return self._client.get_vault(vault_id)

    def get_all_vaults(self) -> List[Dict[str, Any]]:
        return self._client.get_vaults()

    def get_all_fees(self) -> List[Dict[str, Any]]:
        return self._client.get_fees()

    def get_transaction(self, transaction_id: str) -> Dict[str, Any]:
        return self._client.get_transaction(transaction_id)

    def get_all_transactions(
        self, tx_type: TransactionType = None
    ) -> List[Dict[str, Any]]:
        return self._client.get_transactions(tx_type=tx_type.value if tx_type else None)

    def deposit(
        self,
        user_id: str,
        asset_id: str,
        amount: int,
        da_mode: DataAvailabilityMode,
        private_key: str,
        token_id: int = None,
        wait_for_receipt: bool = False,
    ):
        deposit_details = self._client.get_deposit_details(
            user_id=user_id,
            asset_id=asset_id,
            amount=str(amount),
            da_mode=da_mode,
            token_id=token_id,
        )

        if deposit_details["assetContractAddress"] is not None:
            # TODO the API should return the approve function name, contract address and parameters.
            # TODO for each tx the API should include a singable payload as well.
            # TODO check allowance and approve if token.
            raise NotImplementedError("Tokens deposits are not supported yet.")

        # TODO the API should return the function parameters in a separate field.
        # TODO check if exists
        deposit_func = self._starkEx.find_functions_by_name(
            deposit_details["depositFunction"]
        )[0]
        tx = deposit_func(
            starkKey=int(deposit_details["starkKey"], 16),
            assetType=int(deposit_details["assetType"], 16),
            vaultId=int(deposit_details["vaultId"]),
        ).build_transaction(
            {
                "value": int(deposit_details["amount"]),
                "nonce": self._web3.eth.get_transaction_count(
                    self._web3.to_checksum_address(
                        get_eth_address_from_private_key(private_key)
                    )
                ),
            }
        )

        # Sign and submit the deposit tx.
        signed_tx = self._web3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_hash = self._web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        # Wait for the tx to be mined.
        if wait_for_receipt:
            tx_receipt = self._web3.eth.wait_for_transaction_receipt(tx_hash)

        # Return the deposit result.
        return {
            "txHash": tx_hash.hex(),
            "status": "CONFIRMED"
            if wait_for_receipt and tx_receipt.status
            else "FAILED"
            if wait_for_receipt
            else "SUBMITTED",
        }

    def transfer(
        self,
        sender_id: str,
        recipient_id: str,
        asset_id: str,
        amount: int,
        sender_da_mode: DataAvailabilityMode,
        recipient_da_mode: DataAvailabilityMode,
        stark_private_key: str,
        token_id: int = None,
    ) -> Dict[str, Any]:
        # Query the StarkExpress API for the transfer details.
        transfer_details = self._client.get_transfer_details(
            sender_id=sender_id,
            receiver_id=recipient_id,
            asset_id=asset_id,
            amount=str(amount),
            sender_da_mode=sender_da_mode,
            receiver_da_mode=recipient_da_mode,
            token_id=token_id,
        )

        # Compute STARK signature for the transfer.
        # TODO encode message locally for trustless operation.
        stark_signature = sign_message(
            message_hash=int(transfer_details["signablePayload"], 16),
            private_key=stark_private_key,
        )

        # Send the transfer request to the StarkExpress API.
        transfer = self._client.transfer(
            sender_vault_id=transfer_details["senderVaultId"],
            receiver_vault_id=transfer_details["receiverVaultId"],
            quantized_amount=transfer_details["quantizedAmount"],
            expiration_timestamp=transfer_details["expirationTimestamp"],
            nonce=transfer_details["nonce"],
            stark_signature=stark_signature,
        )

        return transfer

    def mint(
        self,
        user_id: str,
        asset_id: str,
        amount: int,
        da_mode: DataAvailabilityMode,
        token_id: int = None,
    ):
        user_mint = {
            "assetId": asset_id,
            "amount": str(amount),
            "dataAvailabilityMode": da_mode.value,
        }
        user_mint.update({"mintingBlob": str(hex(token_id))} if token_id else {})

        return self._client.mint(users=[{"userId": user_id, "mints": [user_mint]}])

    def withdraw(
        self,
        user_id: str,
        asset_id: str,
        amount: int,
        da_mode: DataAvailabilityMode,
        token_id: int = None,
    ):
        # TODO get user vaults from the API.
        # TODO find matching vault based on asset_id and da_mode.
        # TODO send withdrawal request to the API.
        user = self.get_user(user_id)

        # Find matching vault based on asset_id and da_mode.
        def get_da_from_vault_id(vault_id: int) -> DataAvailabilityMode:
            return (
                DataAvailabilityMode.VALIDIUM
                if vault_id <= 2147483648
                else DataAvailabilityMode.ZK_ROLLUP
            )

        vaults = user["vaultsPerAsset"].get(asset_id, None)
        if vaults is None:
            return {}  # TODO raise exception
        vaults = list(
            filter(
                lambda v: get_da_from_vault_id(int(v["vaultChainId"])).value
                == da_mode.value,
                vaults,
            )
        )
        vaults = list(sorted(vaults, key=lambda v: int(v["vaultChainId"])))

        # Validate available balance.
        total_balance = sum(map(lambda v: int(v["availableBalance"]), vaults))
        if total_balance < amount:
            return {}  # TODO raise exception

        withdrawn = 0
        result = []
        while withdrawn < amount:
            vault = vaults.pop(0)
            vault_withdraw_amount = min(
                amount - withdrawn, int(vault["availableBalance"])
            )
            result.append(
                self._client.withdraw(
                    vault_id=vault["vaultId"], amount=str(vault_withdraw_amount)
                )
            )
            withdrawn += vault_withdraw_amount

        return result
