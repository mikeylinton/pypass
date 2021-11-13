import json, base64, pyperclip, getpass, uuid; 
from cryptography.fernet import Fernet;
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC;
from cryptography.hazmat.primitives import hashes;
from InquirerPy import prompt;
from InquirerPy.validator import PathValidator;
class Data:
    def __init__(self, file):
        self.file=file
        self.load
        

    @property
    def load(self):
        data=json.load(open(self.file, 'r'))
        self.settings=data['settings']
        self.content=data['items']

    @property
    def save(self):
        data={}
        data['settings']=self.settings
        data['items']=self.content
        with open(self.file,'r+') as file:
            json.dump(data, file, indent=4)

    @property
    def names(self):
        return [[x['UUID'],x['name']] for x in self.content]

    def add(self, entry):
        items=self.content
        items.append(entry)
        self.content=items

class Crypto:
    def __init__(self):
        password = bytes(getpass.getpass('Master password:'), 'utf-8')
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
        input('Password saved to clipboard, press return to clear.')
        pyperclip.copy('')
        
def getEntry(data,crypto):
    select = [
    {
        'type': 'list',
        'name': 'option',
        'message': 'What would you like to do?',
        'choices': data.names
    },
    ]
    UUID=prompt(select)['option'][0]
    for x in data.content:
        if x['UUID']==UUID:
            username=x['username']
            password=x['password']
            break
    pyperclip.copy(username)
    print('Username: '+username)
    input('Username saved to clipboard, press return to get password.')
    pyperclip.copy(crypto.decrypt(password))
    input('Password saved to clipboard, press return to clear clipboard.')

def addEntry(data,crypto):
    questions = [
    {"type": "input", "message": "Entry name?", "name": "name"},
    {"type": "input", "message": "URI?", "name": "uri"},
    {"type": "input", "message": "Username?", "name": "username"}
    ]
    entry=prompt(questions)
    entry['password']=crypto.encrypt(getpass.getpass('Password:'))
    entry['UUID']=str(uuid.uuid4())
    data.add(entry)
    data.save

def importData(data,crypto):
    select = [
    {
        'type': 'list',
        'name': 'option',
        'message': 'Import from?',
        'choices': [
            'Bitwarden',
            'Back'
        ]
    },
    {
        "message": "Enter the filepath to upload:",
        "type": "filepath",
        "name": "filepath",
        "validate": PathValidator(),
        "only_files": True,
    }
    ]
    result=prompt(select)
    option=result['option']
    filepath=result['filepath']
    if option=='Bitwarden':
        external_data=json.load(open(filepath, 'r'))["items"]
        for x in external_data:
            items={}
            items['name']=x['name']
            items['uri']=x['login']['uris'][0]['uri']
            items['username']=x['login']['username']
            items['password']=crypto.encrypt(x['login']['password'])
            items['UUID']=x['id']
            data.add(items)
        data.save

if __name__ == '__main__':
    file=str('pypass.json')
    select = [
    {
        'type': 'list',
        'name': 'option',
        'message': 'What would you like to do?',
        'choices': [
            'Get login',
            'Add login',
            'Import data',
            'Exit'
        ]
    },
    ]
    option=prompt(select)['option']
    if option=='Exit':
        exit()
    else:
        data=Data(file)
        crypto=Crypto()
    if option=='Get login':
        getEntry(data,crypto)
    elif option=='Add login':
        addEntry(data,crypto)
    elif option=='Import data':
        importData(data,crypto)
    while True:
        option=prompt(select)['option']
        if option=='Exit':
            exit()
        elif option=='Get login':
            getEntry(data,crypto)
        elif option=='Add login':
            addEntry(data,crypto)
        elif option=='Import data':
            importData(data,crypto)