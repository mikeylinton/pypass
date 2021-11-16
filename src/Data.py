import json, os
class Data:
    def __init__(self):
        self._filepath='pypass.json'

    @property
    def filepath(self):
        return self._filepath
    
    @filepath.setter
    def filepath(self,value):
        self._filepath=value

    @property
    def load(self):
        with open(self.filepath,'r') as f:
            lines=f.readlines()
        self.content=''.join(lines)

def fileExists(filepath):
    return os.path.exists(filepath)

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