import json, uuid, getpass, os
from Crypto import Crypto
class Data:
    def __init__(self, filepath):
        self.filepath=filepath
        
    def load(self, crypto):
        with open(self.filepath,'r') as f:
            lines=f.readlines()
        enc=''.join(lines)
        content=crypto.decrypt(enc)
        print(content)
        data=json.loads(content)
        self.config=data["config"]
        self.items=data["items"]

    def add(self, item):
        items=self.items
        items.append(item)
        self.items=items

def fileExists(filepath):
    return os.path.exists(filepath)

def initDataFile(filepath):
    match=False
    while not match:
        print("Master password.")
        crypto=Crypto()
        print("Confirm password.")
        if crypto.key==crypto.keygen:
            match=True
            print("Password updated.")
        else:
            print("Passwords do not match!")
    data='{"config":[],"items":[]}'
    with open(filepath,'w') as f:
        f.write(crypto.encrypt(data))

def saveData(data,crypto):
    newData={}
    newData["config"]=data.config
    newData["items"]=data.items
    with open(data.filepath,'w') as f:
        f.write(crypto.encrypt(newData))

def importData(data,crypto,result):
    option=result['import']
    filepath=result['filepath']
    if option=='Bitwarden (unencrypted)':
        external_data=json.load(open(filepath, 'r'))['items']
        for x in external_data:
            if x['type']!=1:
                continue
            items={}
            items["name"]=x["name"]
            items["uri"]=x["login"]["uris"][0]["uri"]
            items["username"]=x["login"]["username"]
            items["password"]=crypto.encrypt(x["login"]["password"])
            items["UUID"]=x["id"]
            data.add(items)
        saveData(data,crypto)

def addEntry(data,crypto,result):
    item={}
    item["name"]=result["loginName"]
    item["username"]=result["loginUsername"]
    item["uri"]=result["loginURI"]
    item["password"]=getpass.getpass("Password:")
    item["UUID"]=str(uuid.uuid4())
    data.add(item)
    saveData(data,crypto)

def loginList(data):
    return [[x["UUID"],x["name"]] for x in data.items]