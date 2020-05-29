import enum

class Type(enum.Enum):
  train = 1
  test = 2

class Image:
  def __init__(self, path,folderName):
    self.path = path
    self.folderName = folderName
    self.data=[]
    self.type = Type
