import sys, os, json, pyperclip, getpass, uuid
from hashlib import sha256
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/src')
from Crypto import *
from Data import *
from CLI import *
   
def saveData(data,crypto,jsonData):
    enc=crypto.encrypt(json.dumps(jsonData))
    with open(data.filepath,'w') as f:
        f.write(enc)

def selectItem(items):
    select = [
    {
        'type': 'list',
        'name': 'option',
        'message': 'What would you like to do?',
        'choices': [[x["UUID"],x["name"]] for x in items]
    },
    ]
    UUID=prompt(select)["option"][0]
    return UUID

def getItem(items):
    UUID=selectItem(items)
    for x in items:
        if x["UUID"]==UUID:
            username=x["username"]
            password=x["password"]
            if username!=None:
                pyperclip.copy(username)
                print('Username: '+username)
                input('Username saved to clipboard, press return to get password.')
            if password!=None:
                pyperclip.copy(password)
                input('Password saved to clipboard, press return to clear clipboard.')
            break

def delItem(items):
    UUID=selectItem(items)
    for x in items:
        if x["UUID"]==UUID:
            items.remove(x)
            break

def createItem(result):
    item={}
    item["name"]=result["loginName"]
    item["username"]=result["loginUsername"]
    item["uri"]=result["loginURI"]
    item["password"]=getpass.getpass("Password:")
    item["UUID"]=str(uuid.uuid4())
    return item

def initDataFile(data):
    match=False
    while not match:
        cryptoA=Crypto('Master password:')
        cryptoB=Crypto('Confirm password:')
        if cryptoA.key==cryptoB.key:
            match=True
            print('Password updated.')
        else:
            print('Passwords do not match!')
    saveData(data,cryptoA,'{"config":[],"items":[]}')

if __name__ == '__main__':
    cli=CLI()
    data=Data()
    result=inquirer(cli.initQuestions)
    if result["init"] == 'Exit':
        exit()
    elif result["init"]=='Select existing file':
        if  result["filepath"]!=None:
            data.filepath=result["filepath"]
    elif result["init"]=='Create new file':
        if result["filepath"]!='':
            data.filepath=result["filepath"]
        if fileExists(data.filepath):
            print('File already exists! Selecting this file.')
        else:
            initDataFile(data)

    crypto=Crypto('Master password:')
    data.load
    jsonData=json.loads(crypto.decrypt(data.content))
    
    while True:
        result=inquirer(cli.mainQuestions)
        option=result["main"]
        if option=='Exit':
            if result["save"]=='Yes':
                saveData(data,crypto,jsonData)
            exit()
        elif option=='Get login':
            getItem(jsonData["items"])
        elif option=='Add login':
            jsonData["items"].append(createItem(result))
        elif option=='Del login':
            delItem(jsonData["items"])
        elif option=='Import data' and result["import"]!='Back':
            importData(data,crypto,result)
        