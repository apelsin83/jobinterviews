

def singleton(class_):
    # boilerplate for singleton decorator

    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class DataLayer():
    __db = None

    def init_db(self, db):
        self.__db = db

    def save(self, id, side, data):
        self.__db.save(id, side, data)

    def get(self, id, side):
        return self.__db.get(id, side)
