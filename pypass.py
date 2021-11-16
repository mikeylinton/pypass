import sys, os, json, base64, pyperclip, getpass
from hashlib import sha256
from InquirerPy import prompt
from InquirerPy.validator import PathValidator
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/src')
from Data import *

   
def getEntry(data,crypto):
    select = [
    {
        'type': 'list',
        'name': 'option',
        'message': 'What would you like to do?',
        'choices': loginList(data)
    },
    ]
    UUID=prompt(select)['option'][0]
    for x in data.items:
        if x['UUID']==UUID:
            username=x['username']
            password=x['password']
            if username!=None:
                pyperclip.copy(username)
                print('Username: '+username)
                input('Username saved to clipboard, press return to get password.')
            if password!=None:
                pyperclip.copy(password)
                input('Password saved to clipboard, press return to clear clipboard.')
            break

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
        ],
        'name': 'init'
    },
    {
        'message': 'Enter the filepath to upload:',
        'type': 'filepath',
        'when': lambda _: _['init'] == 'Select existing file',
        'validate': PathValidator(),
        'only_files': True,
        'name': 'filepath'
    },
    {
        'message': 'Enter the file name, press return to use default:', 
        'type': 'input', 
        'when': lambda _: _['init'] == 'Create new file',
        'name': 'filepath'
    }
    ]

    try:
        result = prompt(questions, vi_mode=True)
    except InvalidArgument:
        print('No available choices')

    if result['init'] == 'Exit':
        exit()
    elif result['filepath']==None:
        pass
    elif result['filepath']=='':
        initDataFile(filepath)
    elif not fileExists(result['filepath']):
        filepath=result['filepath']
        initDataFile(filepath)
    else:
        filepath=result['filepath']

    crypto=Crypto()
    data=Data(filepath)
    data.load(crypto)
    
    questions = [
    {
        'message': 'What would you like to do?',
        'type': 'list',
        'choices': [
            'Get login',
            'Add login',
            'Import data',
            # 'Settings',
            'Exit'
        ],
        'name': 'main'
    },
    {
        'message': 'Import from?',
        'type': 'list',
        'when': lambda _: _['main'] == 'Import data',
        'name': 'import',
        'choices': [
            'Bitwarden (unencrypted)',
            'Back'
        ]
    },
    {
        'message': 'Enter the filepath to upload:',
        'type': 'filepath',
        'when': lambda _: _['main'] == 'Import data' and _['import'] != 'Back',
        'name': 'filepath',
        'validate': PathValidator(),
        'only_files': True
    },
    # {
    #     'message': 'What would you like to do?',
    #     'type': 'list',
    #     'when': lambda _: _['main'] == 'Settings',
    #     'choices': [
    #         'Change Password',
    #         'Back'
    #     ],
    #     'name': 'settings'
    # },
    {'type': 'input', 'when': lambda _: _['main'] == 'Add login', 'message': 'Entry name?', 'name': 'loginName'},
    {'type': 'input', 'when': lambda _: _['main'] == 'Add login', 'message': 'URI?', 'name': 'loginURI'},
    {'type': 'input', 'when': lambda _: _['main'] == 'Add login', 'message': 'Username?', 'name': 'loginUsername'}
    ]
    while True:
        try:
            result = prompt(questions, vi_mode=True)
        except InvalidArgument:
            print('No available choices')
        option=result['main']
        if option=='Exit':
            exit()
        elif option=='Get login':
            getEntry(data,crypto)
        elif option=='Add login':
            addEntry(data,crypto,result)
        elif option=='Import data' and result['import']!='Back':
            importData(data,crypto,result)
        