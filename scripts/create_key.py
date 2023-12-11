# create_key.py

import os
from pathlib import Path
from secrets import token_bytes

from bson import json_util
from bson.binary import STANDARD
from bson.codec_options import CodecOptions
from pymongo import MongoClient
from pymongo.encryption import ClientEncryption
from pymongo.encryption_options import AutoEncryptionOpts

from dotenv import load_dotenv

load_dotenv()

# Generate a secure 96-byte secret key:
key_bytes = token_bytes(96)

# Configure a single, local KMS provider, with the saved key:
kms_providers = {"local": {"key": key_bytes}}
csfle_opts = AutoEncryptionOpts(
    kms_providers=kms_providers, key_vault_namespace="csfle_demo.__keystore"
)

# Connect to MongoDB with the key information generated above:
with MongoClient(os.environ["MONGODB_URI"], auto_encryption_opts=csfle_opts) as client:
    print("Resetting demo database & keystore ...")
    # client.drop_database("csfle_demo")

    # Create a ClientEncryption object to create the data key below:
    client_encryption = ClientEncryption(
        kms_providers,
        "csfle_demo.__keystore",
        client,
        CodecOptions(uuid_representation=STANDARD),
    )

    print("Creating key in MongoDB ...")
    key_id = client_encryption.create_data_key("local", key_alt_names=["example"])
