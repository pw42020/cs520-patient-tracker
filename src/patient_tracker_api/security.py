"""file with function to encrypt data as it leaves API 
"""
import json
import sys

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

import base64

MAX_BYTES: int = 117


def get_public_key(public_key: str) -> RSA.RsaKey:
    """gets public key from string

    Parameters
    ----------
    public_key : str
        public key as string

    Returns
    -------
    RSA.RsaKey
        public key
    """
    return RSA.importKey(public_key)


def encrypt_data(data: dict[str, str], public_key: RSA.RsaKey) -> bytes:
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

    cipher = PKCS1_v1_5.new(public_key)
    total_encrypted_message = [
        cipher.encrypt(
            byte_package[
                i : i + MAX_BYTES
                if i + MAX_BYTES < len(byte_package)
                else len(byte_package) - 1
            ]
        ).hex()
        for i in range(0, len(byte_package), MAX_BYTES)
    ]
    # retroactively add last part missed if there was a part missed
    total_encrypted_message.append(
        cipher.encrypt(byte_package[-(len(byte_package) % MAX_BYTES) :]).hex()
    )
    print("".join(total_encrypted_message))
    return "".join(total_encrypted_message)
