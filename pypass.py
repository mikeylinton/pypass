import json, base64, pyperclip, getpass, uuid, os; 
from cryptography.fernet import Fernet;
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC;
from cryptography.hazmat.primitives import hashes;
from hashlib import sha256;
from InquirerPy import prompt;
from InquirerPy.validator import PathValidator;
class Data:
    def __init__(self, filepath):
        self.filepath=filepath
        self.load
        

    @property
    def load(self):
        data=json.load(open(self.filepath, 'r'))
        self.config=data['config'][0]
        self.content=data['items']

    @property
    def save(self):
        data={}
        data['config']=self.config
        data['items']=self.content
        with open(self.filepath,'r+') as file:
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
        self.key=self.keygen

    @property
    def keygen(self):
        password = bytes(getpass.getpass('Master password:'), 'utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=password,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    def encrypt(self, secret):
        secret = bytes(secret, 'utf-8')
        f = Fernet(self.key)
        return f.encrypt(secret).decode('utf-8')

    def decrypt(self, secret):
        secret = bytes(secret, 'utf-8')
        f = Fernet(self.key)
        try:
            pyperclip.copy(f.decrypt(secret).decode('utf-8'))
            input('Password saved to clipboard, press return to clear clipboard.')
        except:
            print('Incorrect password, make sure you entered the correct password.')
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
            if username!=None:
                pyperclip.copy(username)
                print('Username: '+username)
                input('Username saved to clipboard, press return to get password.')
            if password!=None:
                crypto.decrypt(password)
            break
    
    

def addEntry(data,crypto):
    questions = [
    {'type': 'input', 'message': 'Entry name?', 'name': 'name'},
    {'type': 'input', 'message': 'URI?', 'name': 'uri'},
    {'type': 'input', 'message': 'Username?', 'name': 'username'}
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
            'Bitwarden (unencrypted)',
            'Back'
        ]
    },
    {
        'message': 'Enter the filepath to upload:',
        'type': 'filepath',
        'name': 'filepath',
        'validate': PathValidator(),
        'only_files': True,
    }
    ]
    result=prompt(select)
    option=result['option']
    filepath=result['filepath']
    if option=='Bitwarden (unencrypted)':
        external_data=json.load(open(filepath, 'r'))['items']
        for x in external_data:
            if x['type']!=1:
                continue
            items={}
            items['name']=x['name']
            items['uri']=x['login']['uris'][0]['uri']
            items['username']=x['login']['username']
            items['password']=crypto.encrypt(x['login']['password'])
            items['UUID']=x['id']
            data.add(items)
        data.save

def verifyToken(data,crypto):
    if sha256(crypto.key).hexdigest()!=data.config['token']:
        print('Invalid token')
        exit()

def fileExists(filepath):
    return os.path.exists(filepath)
def selectExistingFile(result):
    return result[0] == 'Select existing file'
def createNewFile(result):
    return result[0] == 'Create new file'

if __name__ == '__main__':
    filepath=str('pypass.json')
    questions = [
    {
        'message': 'Default file not found! What would you like to do?',
        'type': 'list',
        'when': lambda _: not os.path.exists(filepath),
        'choices': [
            'Select existing file',
            'Create new file',
            'Exit'
        ]
    },
    {
        'message': 'Enter the filepath to upload:',
        'type': 'filepath',
        'when': lambda _: _[0] == 'Select existing file',
        'validate': PathValidator(),
        'only_files': True,
        'name': 'filepath'
    },
    {
        'message': 'Enter the file name, press return to use default:', 
        'type': 'input', 
        'when': lambda _: _[0] == 'Create new file',
        'name': 'filepath'
    }
    ]

    try:
        result = prompt(questions, vi_mode=True)
    except InvalidArgument:
        print('No available choices')
    
    if result[0] == 'Exit':
        exit()
    elif result['filepath']==None:
        pass
    elif result['filepath']=='':
        crypto=Crypto()
        with open(filepath,'w') as f:
            f.write('{"config": [{"token": "'+sha256(crypto.key).hexdigest()+'"}],"items":[]}')
    elif not fileExists(result['filepath']):
        filepath=result['filepath']
        crypto=Crypto()
        with open(filepath,'w') as f:
            f.write('{"config": [{"token": "'+sha256(crypto.key).hexdigest()+'"}],"items":[]}')
    else:
        filepath=result['filepath']

    questions = [
    {
        'message': 'What would you like to do?',
        'type': 'list',
        'choices': [
            'Get login',
            'Add login',
            'Import data',
            'Exit'
        ],
        'name': 'option'
    },
    ]
    option=prompt(questions)['option']
    if option=='Exit':
        exit()
    else:
        data=Data(filepath)
        crypto=Crypto()
        verifyToken(data,crypto)
    if option=='Get login':
        getEntry(data,crypto)
    elif option=='Add login':
        addEntry(data,crypto)
    elif option=='Import data':
        importData(data,crypto)
    while True:
        option=prompt(questions)['option']
        if option=='Exit':
            exit()
        elif option=='Get login':
            getEntry(data,crypto)
        elif option=='Add login':
            addEntry(data,crypto)
        elif option=='Import data':
            importData(data,crypto)