import os
import base64
import json

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Crypto:
    def __init__(self):
        self.__key = None

    def password_comp(self, password_a, password_b):
        if password_a == password_b:
            self.key = password_a
            return True
        else:
            return False

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, value):
        self.__key = self.keygen(value)

    def encrypt(self, plaintext):
        byts = bytes(str(plaintext), 'utf-8')
        f = Fernet(self.key)
        return f.encrypt(byts).decode('utf-8')

    def decrypt(self, ciphertext):
        byts = bytes(str(ciphertext), 'utf-8')
        f = Fernet(self.key)
        return f.decrypt(byts).decode('utf-8')

    def keygen(self, value):
        password = bytes(value, 'utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=password,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password))


class FileData:
    def __init__(self):
        self._filepath = './pypass.json'
        self._content = ""

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        self._filepath = value


def fileExists(filepath):
    return os.path.exists(filepath)


def load(crypto: Crypto):
    with open(FileData.filepath.__str__(), 'r') as f:
        lines = f.readlines()
        FileData.content_getter = crypto.decrypt(''.join(lines))


def save(crypto: Crypto, json_data):
    ciphertext = crypto.encrypt(json.dumps(json_data))
    with open(FileData.filepath.__str__(), 'w') as f:
        f.write(ciphertext)
