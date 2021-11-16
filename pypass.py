import sys, os, json, base64, pyperclip, getpass, uuid
from hashlib import sha256
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/src')
from Crypto import *
from Data import *
from CLI import *
   
def saveData(jsonData,crypto):
    enc=crypto.encrypt(json.dumps(jsonData))
    with open(filepath,'w') as f:
        f.write(enc)

def getItem(items):
    select = [
    {
        'type': 'list',
        'name': 'option',
        'message': 'What would you like to do?',
        'choices': [[x["UUID"],x["name"]] for x in items]
    },
    ]
    UUID=prompt(select)['option'][0]
    for x in items:
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

def createItem(result):
    item={}
    item["name"]=result["loginName"]
    item["username"]=result["loginUsername"]
    item["uri"]=result["loginURI"]
    item["password"]=getpass.getpass("Password:")
    item["UUID"]=str(uuid.uuid4())
    return item

def initDataFile(filepath):
    match=False
    while not match:
        cryptoA=Crypto('Master password:')
        cryptoB=Crypto('Confirm password:')
        if cryptoA.key==cryptoB.key:
            match=True
            print('Password updated.')
        else:
            print('Passwords do not match!')
    saveData('{"config":[],"items":[]}',cryptoA)

if __name__ == '__main__':
    cli=CLI()
    filepath=cli.defaultFile

    result=inquirer(cli.initQuestions)
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

    crypto=Crypto('Master password:')
    data=Data(filepath)
    jsonData=json.loads(crypto.decrypt(data.content))
    
    while True:
        print(jsonData)
        result=inquirer(cli.mainQuestions)
        option=result['main']
        if option=='Exit':
            saveData(jsonData,crypto)
            exit()
        elif option=='Get login':
            getItem(jsonData["items"])
        elif option=='Add login':
            jsonData["items"].append(createItem(result))
        elif option=='Import data' and result['import']!='Back':
            importData(data,crypto,result)
        