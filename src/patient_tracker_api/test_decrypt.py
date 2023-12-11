# attempt to decrypt decrypt.py using private.pem
import json

import rsa
from security import encrypt_data

MAX_BYTES = 128
# create list of only every two characters and treat values as hex
with open("../../assets/default_patient.json", "r") as f:
    patient_json = json.loads(f.read())

# encrypt with public key
with open("../../assets/public.pem", "r") as f:
    public_key: str = f.read()
    public_key = rsa.PublicKey.load_pkcs1(public_key.encode())

# encrypt data
data = encrypt_data(patient_json, public_key)
print(data)

# decrypt with private key
with open("../../assets/private.pem", "r") as f:
    private_key: str = f.read()
    private_key = rsa.PrivateKey.load_pkcs1(private_key.encode())

total_encrypted_message = []

print(len(data))
for i in range(0, len(data), MAX_BYTES):
    total_encrypted_message.append(data[i : i + MAX_BYTES])

print(
    b"".join(
        [
            rsa.decrypt(
                small_data,
                private_key,
            )
            for small_data in total_encrypted_message
        ]
    )
)

# print(b"".join(total_encrypted_message))
