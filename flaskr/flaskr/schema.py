"Modulo de prueba para creacion de schemas "

from pymongo import MongoClient

def add():
    client = MongoClient()
    db = client.flaskr

    entry = {"title": "Sample entry", "text":"Sample text"}
    entries = db.entries
    entry_id = entries.insert_one(entry).inserted_id
    
    print(entry_id)
    client.close()

def find():
    client = MongoClient()
    db = client.flaskr
    entries = db.entries
    res = entries.find()
    arr = []
    for entry in res:
        arr.append(entry)
    print(arr)
    # print(res)
    client.close()

if __name__ == "__main__":
    add()

