from bson import ObjectId

def objectid_to_str(obj):
    """
    Convierte todos los ObjectId de un documento de MongoDB a cadenas (str).
    """
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {key: objectid_to_str(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [objectid_to_str(item) for item in obj]
    else:
        return obj
