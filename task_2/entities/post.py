from bson import ObjectId


class Post:
    def __init__(
        self,
        author_name: str,
        author_link: str | None,
        quote: str,
        tags: list[str],
        _id: str | None = None,
    ):
        self._id = ObjectId() if not _id else ObjectId(_id)
        self.author_name = author_name
        self.author_link = author_link
        self.quote = quote
        self.tags = tags

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
            f"Post("
            f"author={self.author_name}, "
            f"link={self.author_link}, "
            f"quote={self.quote}, "
            f"tags={self.tags}) "
        )
