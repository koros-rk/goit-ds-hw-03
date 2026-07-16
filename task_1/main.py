import os

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class Cat:
    def __init__(
        self, name: str, age: int, features: list[str], _id: str | None = None
    ):
        self._id = ObjectId() if not _id else ObjectId(_id)
        self.name = name
        self.age = age
        self.features = features

    def dump(self):
        return self.__dict__

    def __repr__(self):
        return f"Cat(name={self.name}, age={self.age}, features={self.features})"


class CatsRepository:
    def __init__(self):
        self._uri = os.getenv("DATABASE_URL")

    def __enter__(self):
        self._client = MongoClient(self._uri)
        self._collection = self._client["cats_db"]["cats"]
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._client.close()

    def save(self, entity: Cat):
        self._collection.insert_one(entity.dump())

    def get_one(self, name: str):
        if entity := self._collection.find_one({"name": name}):
            return Cat(**entity)
        raise ValueError("Cat not found")

    def get_all(self):
        entities = self._collection.find()
        return [Cat(**entity) for entity in entities]

    def delete_one(self, name: str):
        if entity := self.get_one(name):
            self._collection.delete_one({"name": entity.name})

    def delete_all(self):
        self._collection.delete_many({})

    def update_age(self, name: str, age: int):
        if entity := self.get_one(name):
            self._collection.update_one(
                {"name": entity.name},
                {"$set": {"age": age}},
            )

    def update_features(self, name: str, new_feature: str):
        if entity := self.get_one(name):
            self._collection.update_one(
                {"name": entity.name},
                {"$set": {"features": [new_feature, *entity.features]}},
            )


if __name__ == "__main__":
    cat = Cat(name="Murzik", age=2, features=["long tail", "friendly"])

    try:
        with CatsRepository() as repo:
            repo.save(cat)
            print(f"Created: {repo.get_one("Murzik")}")

            print(f"All cats: {repo.get_all()}")

            repo.update_age("Murzik", 3)
            print(f'Updated age: {repo.get_one("Murzik")}')

            repo.update_features("Murzik", "long legs")
            print(f'Updated feature: {repo.get_one("Murzik")}')

            repo.delete_one("Murzik")
            print(f'Deleted: {repo.get_one("Murzik")}')

    except ValueError as e:
        print(f"Cats Repository error: {e}")
    except Exception as e:
        print(e)
