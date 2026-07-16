import os
from dotenv import load_dotenv
from pymongo import MongoClient

from entities.post import Post

load_dotenv()


class PostsRepository:
    def __init__(self):
        self._uri = os.getenv("DATABASE_URL")

    def __enter__(self):
        self._client = MongoClient(self._uri)
        self._collection = self._client["blog_db"]["posts"]
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._client.close()

    def save(self, entity: Post):
        self._collection.insert_one(entity.dump())

    def save_many(self, entity: list[Post]):
        self._collection.insert_many([entity.dump() for entity in entity])

    def cleanse(self):
        self._collection.delete_many({})
