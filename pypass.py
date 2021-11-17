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
    items=[[x["UUID"],x["name"]] for x in items]
    items.insert(0,'Back')
    pass
    select = [
    {
        'type': 'list',
        'message': 'What would you like to do?',
        'choices': items
    },
    ]
    result=prompt(select)[0]
    print()
    if result=='Back':
        return None
    else:
        return result[0]

def getItem(items):
    UUID=selectItem(items)
    if UUID!=None:
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
    if UUID!=None:
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

def importItems(result):
    option=result['import']
    filepath=result['filepath']
    items=[]
    if option=='Bitwarden (unencrypted)':
        data=json.load(open(filepath, 'r'))['items']
        for x in data:
            if x['type']==1:
                item={}
                item["name"]=x["name"]
                item["uri"]=x["login"]["uris"][0]["uri"]
                item["username"]=x["login"]["username"]
                item["password"]=x["login"]["password"]
                item["UUID"]=x["id"]
                items.append(item)
    return items

def initDataFile(data):
    match=False
    while not match:
        cryptoA=Crypto('Master password:')
        cryptoB=Crypto('Confirm password:')
        if cryptoA.key==cryptoB.key:
            match=True
            color_print([(cli.colour["Success"], 'Password updated.')])
        else:
            color_print([(cli.colour["Alert"], 'Passwords do not match!')])
    saveData(data,cryptoA,'{"config":[],"items":[]}')

if __name__ == '__main__':
    cli=CLI()
    data=Data()
    result=inquirer(cli.initQuestions)
    if result["init"] == 'Exit':
        exit()
    elif result["upload"]!=None:
        data.filepath=result["upload"]
    elif result["create"]!=None:
        if result["create"]!='':
            data.filepath=result["create"]
        if fileExists(data.filepath):
            color_print([(cli.colour["Warning"], 'File already exists! Selecting this file.')])
        else:
            initDataFile(data)

    crypto=Crypto('Master password:')
    data.load

    try:
        jsonData=json.loads(crypto.decrypt(data.content))
    except InvalidToken:
        color_print([(cli.colour["Alert"], 'Incorrect password!')])
        exit()
    
    while True:
        result=inquirer(cli.mainQuestions)
        option=result["main"]
        if option=='Exit':
            if result["save"]!='Cancel':
                if result["save"]=='Yes':
                    saveData(data,crypto,jsonData)
                exit()
        elif option=='Get login':
            getItem(jsonData["items"])
        elif option=='Add login':
            if result['loginName']=='':
                print('Name required!')
            elif result['loginUsername']=='':
                print('Username required!')
            else:
                jsonData["items"].append(createItem(result))
        elif option=='Del login':
            delItem(jsonData["items"])
        elif option=='Import data' and result["import"]!='Back':
            jsonData["items"].extend(importItems(result))
        