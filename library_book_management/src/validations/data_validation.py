from models.schemas import Response

def isnone(_books):
    if _books == None:
        return True
    else:
        return False