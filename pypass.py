import sys, os, json, base64, pyperclip, getpass
from hashlib import sha256
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/src')
from Data import *
from CLI import *
   
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
    cli=CLI()
    result=inquirer(cli.initQuestions)
    print(result)
    filepath=cli.defaultFile
    if result['init'] == 'Exit':
        exit()
    elif result['init']=='Select existing file':
        if  result['filepath']!=None:
            filepath=result['filepath']
    elif result['init']=='Create new file':
        if result['filepath']!='':
            filepath=result['filepath']
            if fileExists(filepath):
                print('File already exists! Selecting this file.')
            else:
                initDataFile(filepath)

    # elif result['filepath']==None:
    #     print('hello')
    #     filepath=cli.defaultFile
    # elif result['filepath']=='':
    #     initDataFile(filepath)
    # elif not fileExists(result['filepath']):
    #     filepath=result['filepath']
    #     initDataFile(filepath)
    # else:
    #     filepath=result['filepath']
    # # crypto=Crypto()
    # # data=Data(filepath)
    # # data.load(crypto)
    # result=inquirer(cli.initQuestions)
    # while True:
    #     try:
    #         result = prompt(questions, vi_mode=True)
    #     except InvalidArgument:
    #         print('No available choices')
    #     option=result['main']
    #     if option=='Exit':
    #         exit()
    #     elif option=='Get login':
    #         getEntry(data,crypto)
    #     elif option=='Add login':
    #         addEntry(data,crypto,result)
    #     elif option=='Import data' and result['import']!='Back':
    #         importData(data,crypto,result)
        