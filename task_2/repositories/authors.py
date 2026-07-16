import os
from dotenv import load_dotenv
from pymongo import MongoClient

from entities.author import Author

load_dotenv()


class AuthorsRepository:
    def __init__(self):
        self._uri = os.getenv("DATABASE_URL")

    def __enter__(self):
        self._client = MongoClient(self._uri)
        self._collection = self._client["blog_db"]["authors"]
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._client.close()

    def save(self, entity: Author):
        self._collection.insert_one(entity.dump())

    def save_many(self, entity: list[Author]):
        self._collection.insert_many([entity.dump() for entity in entity])

    def cleanse(self):
        self._collection.delete_many({})
