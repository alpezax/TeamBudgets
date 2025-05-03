def run():
    import os
    from pymongo import MongoClient
    from pymongo.errors import BulkWriteError
    from dotenv import load_dotenv

    # Cargar configuración desde .env
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME_ORIGEN = os.getenv("DB_NAME")
    DB_NAME_DESTINOS = [
        os.getenv("DB_NAME_PRE"),
        os.getenv("DB_NAME_TST1"),
        os.getenv("DB_NAME_TST2"),
        os.getenv("DB_NAME_TST3")
    ]

    def get_db(mongo_uri, db_name):
        client = MongoClient(mongo_uri)
        return client[db_name]

    print(f"🔧 Iniciando migración desde '{DB_NAME_ORIGEN}' a destinos: {', '.join(DB_NAME_DESTINOS)}")

    origin_db = get_db(MONGO_URI, DB_NAME_ORIGEN)
    dest_dbs = [get_db(MONGO_URI, name) for name in DB_NAME_DESTINOS]

    collection_names = origin_db.list_collection_names()

    for name in collection_names:
        origin_collection = origin_db[name]
        documents = list(origin_collection.find({}))

        if not documents:
            print(f"🟡 {name}: colección vacía.")
            continue

        print(f"\n🔄 Migrando colección: {name} ({len(documents)} documentos)")

        for dest_db, dest_name in zip(dest_dbs, DB_NAME_DESTINOS):
            dest_collection = dest_db[name]
            existing_ids = set(doc["_id"] for doc in dest_collection.find(
                {"_id": {"$in": [doc["_id"] for doc in documents]}}, {"_id": 1}
            ))
            new_docs = [doc for doc in documents if doc["_id"] not in existing_ids]

            if not new_docs:
                print(f"  → {dest_name}: sin documentos nuevos.")
                continue

            try:
                dest_collection.insert_many(new_docs, ordered=False)
                print(f"  ✅ {dest_name}: {len(new_docs)} documentos insertados.")
            except BulkWriteError as bwe:
                print(f"  ⚠️ {dest_name}: error en inserción: {bwe.details}")

    print("\n✅ Migración completada.")

# Si deseas ejecutar directamente:
# run()
