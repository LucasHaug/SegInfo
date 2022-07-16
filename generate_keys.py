from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from common import PRIVATE_ASYM_KEY_FILE_NAME, PUBLIC_ASYM_KEY_FILE_NAME

# Generate private_key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Generate public_key
public_key = private_key.public_key()

# Save serialized private_key to file
serial_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open(PRIVATE_ASYM_KEY_FILE_NAME, 'wb') as f: f.write(serial_private)

# Save serialized public_key to file
serial_pub = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open(PUBLIC_ASYM_KEY_FILE_NAME, 'wb') as f: f.write(serial_pub)