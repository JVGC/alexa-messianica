import os
from pymongo import MongoClient
from models.experience import Experience


class ExperienceMongoRepository:
    def __init__(self) -> None:
        mongo_user = os.getenv("MONGO_USER")
        mongo_password = os.getenv("MONGO_PASSWORD")
        mongo_url = os.getenv("MONGO_CLUSTER_URL")
        mongo_host = f"mongodb+srv://{mongo_user}:{mongo_password}{mongo_url}/?retryWrites=true&w=majority"
        client = MongoClient(mongo_host)
        self._db = client["Messianic"]
        print("Mongo Connectado")

    def create(
        self,
        date: str,
        person_name: str,
        church: str,
        content: str,
        audio_url: str,
        url: str,
    ) -> Experience:
        experience_obj = {
            "date": date,
            "person_name": person_name,
            "church": church,
            "content": content,
            "audio_url": audio_url,
            "url": url,
        }
        result_id = self._db["experiences"].insert_one(experience_obj).inserted_id

        return self._db["experiences"].find_one(filter={"_id": result_id})

    def getById(self, _id: str) -> Experience:
        return self._db["experiences"].find_one(filter={"_id": _id})

    def getByDate(self, date: str) -> Experience:
        return self._db["experiences"].find_one(filter={"date": date})

    def deleteByDate(self, date: str) -> Experience:
        return self._db["experiences"].delete_one(filter={"date": date})
