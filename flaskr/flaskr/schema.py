"Modulo de prueba para creacion de schemas "

from pymongo import MongoClient

def main():
    client = MongoClient()
    db = client.flaskr

    entry = {"title": "Sample entry"}
    entries = db.entries
    entry_id = entries.insert_one(entry).inserted_id
    
    print(entry_id)
    client.close()

if __name__ == "__main__":
    main()

