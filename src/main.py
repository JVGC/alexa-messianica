from datetime import date
from dotenv import load_dotenv
from mongo.experience_repository import ExperienceMongoRepository


def main():
    experience_repository = ExperienceMongoRepository()

    experience = experience_repository.create(
        date=date.today().strftime(format="%d/%m/%Y"),
        person_name="João",
        church="JC Mogi Mirim",
        content="This is my Experience",
        audio_url="some url",
        url="some url",
    )
    print(experience)


if __name__ == "__main__":
    load_dotenv()
    main()
