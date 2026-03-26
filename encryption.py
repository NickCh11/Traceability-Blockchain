from cryptography.fernet import Fernet
import json
import os
import base64


def generate_encyption_key():
    if os.path.exists('encryption_key.key'):
        with open('encryption_key.key', 'rb') as key_file:
            # print('existing encryption key')
            return Fernet(key_file.read())
    else:
        key = Fernet.generate_key()
        with open('encryption_key.key', 'wb') as key_file:
            key_file.write(key)
        # print('not existing encryption key')
        return Fernet(key_file.read())


# Data encryption
def encrypt_data(encryption_key, data):
    json_data = json.dumps(data).encode()
    encrypted_data = encryption_key.encrypt(json_data)
    return base64.b64encode(encrypted_data)  # Κωδικοποίηση των bytes ως base64 string


# Data decryption
def decrypt_data(encryption_key, encrypted_data):
    decoded_encrypted_data = base64.b64decode(encrypted_data)  # Αποκωδικοποίηση του base64 string σε bytes
    decrypted_data = encryption_key.decrypt(decoded_encrypted_data)
    return json.loads(decrypted_data.decode())
