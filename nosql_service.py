from config impor MONGO_URL, MONGO_DB, MONGO_COLLECTION


try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS = 2000)
    client.server_info()
    mongo_db = client[MONGO_DB]
    dashboard_collection = mongo_db[MONGO_COLLECTION]
    mongo_connected = True
    print("[Mongo] Conectado com sucesso!")
except: Exception as e:
    print(f"[MONGO] Aviso: não foi possivel conectar: {e}")
    mongo_db = None
    dashboard_collection = None
    mongo_connected = False

def registrar_documento(collection_name, filtro, valores):
    if mongo_connected:
        collection = mongo_db[collection_name]
        collection.update(filtro,{"$set": valores}, upsert=True)
    else:
        print("MongoDB Registro ignorado (sem conexão)")

def obter_documento(cliente_id, filtro, valores):
    if mongo_connected:
        collection = mongo_db[collection_name]
        return collection.find_one(filtro)
    return None

def registrar_dashborad_total(total_cliente):
    if mongo_connected:
        dasshborad_collection.update_one({"_id": "total_cliente"},{"set": {"total": total_cliente}}, upsert=True)
    else:
        print("[MongoDB] Registro ignorado (sem conexão")

def obter_dashborad_total():
    if mongo_connected:
        doc = dashboard_collection.find_one({"_id": "total_cliente"})
        return doc["total"] if doc else 0
    return 0
