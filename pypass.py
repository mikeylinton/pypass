import json, base64, os, pyperclip, getpass; 
from cryptography.fernet import Fernet;
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC;
from cryptography.hazmat.primitives import hashes;
from InquirerPy import prompt;
class Data:
    def __init__(self, file):
        self.file=file
        self.content=json.load(open(self.file, 'r'))
        

    @property
    def load(self):
        self.content=json.load(open(self.file, 'r'))

    def password(self,search):
        for item in self.content['items']:
            if item['name']==search:
                print('Username:'+item['username'])
                return item['password']
                break
    @property
    def names(self):
        return [x['name'] for x in self.content['items']]

class Crypto:
    def __init__(self, password):
        password = bytes(password, 'utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=password,
            iterations=100000,
        )
        self.key=base64.urlsafe_b64encode(kdf.derive(password))

    def encrypt(self, secret):
        secret = bytes(secret, 'utf-8')
        f = Fernet(self.key)
        return f.encrypt(secret).decode('utf-8')

    def decrypt(self, secret):
        secret = bytes(secret, 'utf-8')
        f = Fernet(self.key)
        pyperclip.copy(f.decrypt(secret).decode('utf-8'))
        input('Password saved to clipboard, press any key to clear.')
        pyperclip.copy('')
        
if __name__ == '__main__':
    file=str('pypass.json')
    data=Data(file)
    crypto=Crypto(getpass.getpass('Master password:'))
    print(data.names)
    questions = [
    {
        'type': 'list',
        'name': 'name',
        'message': 'Which login?',
        'choices': data.names
    },
    ]
    name=prompt(questions)['name']
    enc=data.password(name)
    crypto.decrypt(enc)