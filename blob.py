



class  Blob:
    
    def __init__(self, data):
        self.data = data
        self.oid = None
    def type(self):
        return "blob"

    def bytedata(self):
       return self.data

    @staticmethod
    def parse(data):
        Blob(data)
