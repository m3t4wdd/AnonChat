from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

def encrypt_message(message, public_key_pem):
    public_key = serialization.load_pem_public_key(public_key_pem.encode())
    encrypted_message = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return bytes(encrypted_message)

def decrypt_message(encrypted_message, private_key_pem):
    private_key = serialization.load_pem_private_key(private_key_pem.encode(), password=None)
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message