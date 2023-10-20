from typing import Any, Dict, Tuple

from coincurve import PublicKey
from eth_account.messages import encode_structured_data
from secrets import token_bytes
from sha3 import keccak_256
from web3 import Web3


def generate_eth_keys() -> Tuple[str, str]:
    """Generate an Ethereum key pair.

    Returns:
        A tuple of the private and public key.
    """
    private_key = keccak_256(token_bytes(32)).digest().hex()
    public_key = PublicKey.from_valid_secret(bytes.fromhex(private_key)).format(
        compressed=False
    )[1:]

    return f"0x{private_key}", f"0x{public_key.hex()}"


def get_eth_address_from_private_key(private_key: str) -> str:
    """Get the Ethereum address from a private key.

    Args:
        private_key: The private_key key.

    Returns:
        The Ethereum address.
    """
    private_key = private_key[2:] if private_key.startswith("0x") else private_key
    private_key = private_key.zfill((len(private_key) + 1) // 2 * 2)
    public_key = PublicKey.from_valid_secret(bytes.fromhex(private_key)).format(
        compressed=False
    )[1:]
    address = keccak_256(public_key).digest()[-20:].hex()

    return Web3().to_checksum_address(address)


# TODO make a generic sign_eip712_message function
def sign_eip712_register_message(data: Dict[str, Any], signer_key: str) -> str:
    msg = {
        "domain": data["domain"],
        "types": data["types"],
        "primaryType": "User",  # TODO: this is hardcoded
        "message": {
            "username": data["message"][0]["value"],
            "address": data["message"][2]["value"],
            "starkKey": data["message"][1]["value"],
        },
    }
    msg["domain"]["chainId"] = int(data["domain"]["chainId"])

    encoded = encode_structured_data(msg)

    signature = Web3().eth.account.sign_message(encoded, signer_key)

    return signature.signature.hex()
