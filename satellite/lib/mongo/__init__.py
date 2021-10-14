from datetime import datetime
from time import time
from pymongo.mongo_client import MongoClient
import config


class MongoConnectionConfig:
    host = config.MONGO_HOST
    database = config.MONGO_DATABASE
    port = config.MONGO_PORT
    user = config.MONGO_USERNAME
    password = config.MONGO_PASSWORD


class MongoConnection:

    def __init__(self, config: MongoConnectionConfig):
        self.db = MongoClient(
            host=config.host, port=config.port).get_database(config.database)
        self.generateConstants()
        pass

    def directGetData(self, colle, id=None, idName: str = "_id", renameId: str = None):
        if type(colle) == str:
            colle = self.db.get_collection(colle)

        if id is None:
            data = colle.find()
        else:
            data = colle.find_one({idName: id})

        output = []

        try:
            for entry in data:
                if not renameId is None:
                    entry[renameId] = entry['_id']
                del entry["_id"]
                output.append(entry)
        except TypeError:
            if data is None:
                return False  # doesnt exist
            else:  # single data
                if not renameId is None:
                    data[renameId] = data['_id']
                del data['_id']
                return data

        return output

    # Initializes the constant values
    def generateConstants(self):
        colle = self.db.get_collection("system_tb")
        try:
            colle.insert_one({
                "_id": "constants",
                "lastAutoincrementId": 1
            })
        except:
            print("already initialized")

    # Returns the last autoincrement id 
    def getLastAutoincrementId(self) -> int:
        data = self.directGetData("system_tb", "constants")
        return data['lastAutoincrementId']

    # Sets the last autoincrement id as what it was provided
    def updateLastAutoincrementId(self, id: int):
        colle = self.db.get_collection("system_tb")
        colle.update_one({"_id": "constants"}, {
            "$set": {"lastAutoincrementId": id}
        })

    # Adds a message on database and returns the generated ID
    def addMessage(self, idMessage: int, value: int, idReference: int = None, dateTime: int = None) -> tuple:

        if idReference is None:
            idReference = self.getLastAutoincrementId() + 1

        if dateTime is None:
            dateTime = int(time())

        colle = self.db.get_collection('references_tb')
        colle.insert_one({
            "_id": idReference,
            "idMessage": idMessage,
            "value": value,
            "idReference": idReference,
            "dateTime": dateTime,
        })

        self.updateLastAutoincrementId(idReference)
        return idReference, dateTime
