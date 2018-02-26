import json
import pymongo

def makeDatabase():
    file = open("PD2.json", "r")
    dictionary = json.loads(file.read())
    file.close()
    connection = pymongo.MongoClient("homer.stuy.edu")
    db = connection["its2010again"]
    collection = db["deck"]
    collection.insert_many(dictionary["cards"])

makeDatabase()