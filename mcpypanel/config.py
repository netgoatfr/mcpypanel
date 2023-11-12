import os
from yaml import load, dump

class Empty:
    pass
class ConfFile:
    def __init__(self,parent,create=False):
        self.parent = parent
        self._datas = {}
        self._create=create
        self._file = parent._DIR+"config.yaml"
        self.log = self.parent.log.get_child("config")
        self.load()
    
    def load(self):
        if not os.path.exists(self._file) and not self._create:
            self.log.fatal("Config file not found! Aborting startup.")
            self.parent._abort_startup = True
            return
        elif  not os.path.exists(self._file) and self._create:
            self.save()
            
        with open(self._file) as f:
            self._datas = load(f)
    def save(self):
        with open(self._file,'w') as f:
            f.write(dump(self._datas))
    
    def __getitem__(self, index):
        if not (type(index) in (str, bytes)):
            raise Exception("a str/bytes must be passed")
        return self._datas.get(index,Empty())
        self.save()
    def __setitem__(self, index, value):
        if not (type(index) in (str, bytes)):
            raise Exception("a str/bytes must be passed")
        self._datas[index] = value
        return self._datas[index]
        self.save()
    def __delattr__(self, index):
        if not (type(index) in (str, bytes)):
            raise Exception("a str/bytes must be passed")
        del self._datas[index]
        self.save()
    def __delitem__(self, index):
        if not (type(index) in (str, bytes)):
            raise Exception("a str/bytes must be passed")
        del self._datas[index]
        self.save()
    def __iter__(self):
        for i in self._datas:
            yield i