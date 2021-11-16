import base64, getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
class Crypto:
    def __init__(self,name):
        self.name=name
        self.key=self.keygen

    @property
    def keygen(self):
        password = bytes(getpass.getpass(self.name), 'utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=password,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    def encrypt(self, plaintext):
        byts = bytes(str(plaintext), 'utf-8')
        f = Fernet(self.key)
        return f.encrypt(byts).decode('utf-8')

    def decrypt(self, ciphertext):
        byts = bytes(str(ciphertext), 'utf-8')
        f = Fernet(self.key)
        return f.decrypt(byts).decode('utf-8')