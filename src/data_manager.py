import os
import base64
import json

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Crypto:
    def __init__(self):
        self.__key = None

    def password_match(self, password, password_check):
        if password == password_check:
            self.key = password
            return True
        else:
            return False

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, value):
        self.__key = keygen(value)

    def encrypt(self, plaintext):
        byts = bytes(plaintext.__str__(), 'utf-8')
        f = Fernet(self.key)
        return f.encrypt(byts).decode('utf-8')

    def decrypt(self, ciphertext):
        byts = bytes(ciphertext.__str__(), 'utf-8')
        f = Fernet(self.key)
        return f.decrypt(byts).decode('utf-8')


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
        return self._filepath.__str__()

    @filepath.setter
    def filepath(self, value):
        self._filepath = value.__str__()


def keygen(value: str):
    password = bytes(value, 'utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=password,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password))


def key_match(key, guess):
    if key == keygen(guess):
        return True
    else:
        return False


def file_exists(filepath: str):
    return os.path.exists(filepath)


def load(crypto: Crypto, data: FileData):
    with open(data.filepath, 'r') as f:
        lines = f.readlines()
    content = ''.join(lines)
    data.content = crypto.decrypt(content)


def save(crypto: Crypto, filepath: str, json_data: dict):
    ciphertext = crypto.encrypt(json.dumps(json_data))
    with open(filepath, 'w') as f:
        f.write(ciphertext)
