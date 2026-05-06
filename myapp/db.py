from pymongo import MongoClient
from django.conf import settings

_client = None

def get_db():
    """Returns a MongoDB database instance (singleton pattern)."""
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGO_URI)
    return _client[settings.MONGO_DB_NAME]

def get_collection(name: str):
    return get_db()[name]