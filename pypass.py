import json
class Main:
    def __init__(self, file):
        self.file=file
        self.content=json.load(open(self.file, 'r'))
        

    @property
    def load(self):
        self.content=json.load(open(self.file, 'r'))

    def find(self,search):
        for item in self.content['items']:
            if item['name']==search:
                print(item['uri'])
                break
    @property
    def names(self):
        return [x['name'] for x in self.content['items']]

if __name__ == '__main__':
    file=str('pypass.json')
    data=Main(file)
    data.find(data.names[1])
    