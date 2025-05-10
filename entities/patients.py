from database import createConn

class patients:
    def __init__(self, name, age, NID):
        self.name = name
        self.age = age
        self.NID = NID
