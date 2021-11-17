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