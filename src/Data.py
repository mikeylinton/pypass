import json, os
class Data:
    def __init__(self, filepath):
        self.filepath=filepath
        self.load
        
    @property
    def load(self):
        with open(self.filepath,'r') as f:
            lines=f.readlines()
        self.content=''.join(lines)

    # def add(self, item):
    #     pass
    #     items=self.items
    #     items.append(item)
    #     self.items=items

def fileExists(filepath):
    return os.path.exists(filepath)

# def saveData(data,crypto):
#     newData={}
#     newData["config"]=data.config
#     newData["items"]=data.items
#     with open(data.filepath,'w') as f:
#         f.write(crypto.encrypt(newData))

# def importData(data,crypto,result):
#     option=result['import']
#     filepath=result['filepath']
#     if option=='Bitwarden (unencrypted)':
#         external_data=json.load(open(filepath, 'r'))['items']
#         for x in external_data:
#             if x['type']!=1:
#                 continue
#             items={}
#             items["name"]=x["name"]
#             items["uri"]=x["login"]["uris"][0]["uri"]
#             items["username"]=x["login"]["username"]
#             items["password"]=crypto.encrypt(x["login"]["password"])
#             items["UUID"]=x["id"]
#             data.add(items)
#         saveData(data,crypto)

# def addEntry(data,crypto,result):
#     item={}
#     item["name"]=result["loginName"]
#     item["username"]=result["loginUsername"]
#     item["uri"]=result["loginURI"]
#     item["password"]=getpass.getpass("Password:")
#     item["UUID"]=str(uuid.uuid4())
#     data.add(item)
#     saveData(data,crypto)

# def loginList(data):
#     return [[x["UUID"],x["name"]] for x in data.items]