"""file with function to encrypt data as it leaves API 
"""
import json
import sys

import rsa
from rsa import PublicKey

MAX_BYTES: int = 117


def get_public_key(public_key: str) -> PublicKey:
    """gets public key from string

    Parameters
    ----------
    public_key : str
        public key as string

    Returns
    -------
    PublicKey
        public key
    """
    return PublicKey.load_pkcs1(public_key.encode())


def encrypt_data(data: dict[str, str], public_key: PublicKey) -> bytes:
    """encrypts data with public key

    Parameters
    ----------
    data : dict[str, str]
        data to encrypt
    public_key : PublicKey
        public key to encrypt data with

    Returns
    -------
    dict[str, bytes]
        encrypted data
    """
    byte_package = json.dumps(data).encode()
    total_encrypted_message = [
        rsa.encrypt(
            byte_package[
                i : i + MAX_BYTES
                if i + MAX_BYTES < len(byte_package)
                else len(byte_package) - 1
            ],
            public_key,
        )
        for i in range(0, len(byte_package), MAX_BYTES)
    ]
    # retroactively add last part missed if there was a part missed
    total_encrypted_message.append(
        rsa.encrypt(byte_package[-(len(byte_package) % MAX_BYTES) :], public_key)
    )
    return b"".join(total_encrypted_message)
