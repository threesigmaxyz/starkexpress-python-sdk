from typing import Tuple

from starkexpress.sdk.crypto.stark.signature import (
    get_random_private_key,
    pedersen_hash as hash_func,
    private_to_stark_key,
    sign,
)

from starkexpress.sdk.crypto.stark.messages import get_transfer_msg


def generate_stark_keys() -> Tuple[str, str]:
    private_key = get_random_private_key()
    public_key = private_to_stark_key(private_key)
    return str(hex(private_key)), str(hex(public_key))


def get_stark_public_key_from_private_key(private_key: str) -> str:
    return str(hex(private_to_stark_key(int(private_key, 16))))


def pedersen_hash(message: str) -> int:
    return hash_func(int(message, 16))


# TODO combine with pedersen_hash
def pedersen_hash_field_elements(*elements: int) -> int:
    return hash_func(*elements)


def sign_message(message_hash: int, private_key: str) -> Tuple[str, str]:
    stark_signature = sign(message_hash, int(private_key, 16))

    return str(hex(stark_signature[0])), str(hex(stark_signature[1]))
