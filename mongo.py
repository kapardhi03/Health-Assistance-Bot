from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://dev:potentia@mgit.dtljue1.mongodb.net/?retryWrites=true&w=majority&appName=mgit"

'''
FN -> fetch_documents

return dict:
 {status: boolean, data : list (of jsons), error : str, code : str}

possible error codes:
    DBE : DATABSE ERROR
'''

'''
FN -> insert_document

return dict:
 {status: boolean, data : str, error : str, code : str}

possible error codes:
    DBE : DATABSE ERROR
'''


'''
FN -> delete_document

return dict:
 {status: boolean, data : str, error : str, code : str}

possible error codes:
    DDE : DOCUMENT DELTE ERROR
'''

def insert_document(database_name, collection_name, document):
    try:
        client = MongoClient("mongodb+srv://dev:potentia@mgit.dtljue1.mongodb.net/?retryWrites=true&w=majority&appName=mgit")
        db = client[database_name]
        collection = db[collection_name]
        collection.insert_one(document)
        client.close()
        return {"status" : True, "data" : "", "error" : "", "code" : ""}
    except Exception as e:
        return {"status" : False, "data" : "", "error" : str(e), "code" : "DBE"}

def fetch_documents(database_name, collection_name, query):
    try:
        client = MongoClient("mongodb+srv://dev:potentia@mgit.dtljue1.mongodb.net/?retryWrites=true&w=majority&appName=mgit")
        db = client[database_name]
        collection = db[collection_name]
        documents = list(collection.find(query))
        client.close()
        return {"status" : True, "data" : documents, "error" : "", "code" : ""}
    except Exception as e:
        {"status" : False, "data" : "", "error" : str(e), "code" : "DBE"}

def delete_collection(database_name, collection_name):
    try:
        client = MongoClient("mongodb+srv://dev:potentia@mgit.dtljue1.mongodb.net/?retryWrites=true&w=majority&appName=mgit")
        db = client[database_name]
        collection = db[collection_name]
        collection.drop()
        return {"status" : True, "data" : "", "error" : "", "code" : ""}
    except Exception as e:
        {"status" : False, "data" : "", "error" : str(e), "code" : "DBE"}

def delete_document(db, collection, query):
    try:
        client = MongoClient("mongodb+srv://dev:potentia@mgit.dtljue1.mongodb.net/?retryWrites=true&w=majority&appName=mgit")
        db = client[db]
        collection = db[collection]
        collection.delete_one(query)
        client.close()
        return {"status" : True, "data" : "", "error" : "", "code" : ""}
    except Exception as e:
        {"status" : False, "data" : "", "error" : str(e), "code" : "DDE"}

def update_document(database_name, collection_name, id_field, id_value, field_to_update, value_to_update):
    try:
        client = MongoClient("mongodb+srv://dev:potentia@mgit.dtljue1.mongodb.net/?retryWrites=true&w=majority&appName=mgit")
        db = client[database_name]
        collection = db[collection_name]
        query = {id_field : id_value}
        new_values = { "$set": {field_to_update: value_to_update} }
        collection.update_one(query, new_values)
        return {"status" : True, "data" : "", "error" : "", "code" : ""}
    except Exception as e:
        {"status" : False, "data" : "", "error" : str(e), "code" : "DBE"}