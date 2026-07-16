from bson import ObjectId


class Author:
    def __init__(
        self,
        fullname: str,
        born_date: str,
        born_location: str,
        description: str,
        _id: str | None = None,
    ):
        self._id = ObjectId() if not _id else ObjectId(_id)
        self.fullname = fullname
        self.born_date = born_date
        self.born_location = born_location
        self.description = description

    def dump(self):
        return self.__dict__

    def serialize(self):
        entity = {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        }

        return {"_id": str(self._id), **entity}

    def __repr__(self):
        return (
            f"Author("
            f"fullname={self.fullname}, "
            f"born_date={self.born_date}, "
            f"born_location={self.born_location}, "
            f"description={self.description})"
        )

    def __str__(self):
        return self.fullname
