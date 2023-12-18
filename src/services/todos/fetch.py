import datetime
import random
import uuid
from time import time

from faker import Faker
from faker.providers import color, currency, date_time, emoji, lorem, misc, person, python

from src.contracts.base import BaseContract
from src.infra.cass.models import blog

fake = Faker("pt_BR")
fake.add_provider(date_time)
fake.add_provider(color)
fake.add_provider(python)
fake.add_provider(emoji)
fake.add_provider(person)
fake.add_provider(misc)
fake.add_provider(lorem)
fake.add_provider(currency)


def generate_todos_week() -> list[dict]:
    return [
        {
            "date": datetime.datetime(day=j, month=9, year=2023).strftime("%Y-%m-%d"),
            "todos": [
                {"id": i, "check": fake.random.choice([True, False]), "description": fake.text(100)}
                for i in range(10)
            ],
        }
        for j in range(1, 6)
    ]


def wrap_chat_message(name: str, message: str) -> dict:
    return {
        "sender": {
            "name": name,
        },
        "color": fake.color(luminosity="light"),
        "timestamp": int(time() * 1000),
        "message": message,
        "type": "USER_TEXT",
    }


def emojify(msg: str) -> str:
    splitted = msg.split(" ")
    for i in range(len(splitted)):
        dice = random.randint(0, 100)
        if dice > 50:
            splitted[i] = f"{fake.emoji()} {splitted[i]} :{fake.word()}:"
    return " ".join(splitted)


def generate_chat() -> dict:
    dice = random.randint(0, 100)

    if dice >= 10:
        return {
            "sender": {
                "name": fake.name(),
            },
            "color": fake.color(luminosity="light"),
            "timestamp": int(time() * 1000),
            "message": emojify(fake.text(100)),
            "type": "USER_TEXT",
        }
    elif dice >= 9:
        return {"timestamp": int(time() * 1000), "type": "GLOBAL_SYNCHRONIZATION"}
    elif dice >= 4:
        return {
            "sender": {
                "name": fake.name(),
            },
            "timestamp": int(time() * 1000),
            "type": "USER_LOGIN",
        }

    return {
        "sender": {
            "name": fake.name(),
        },
        "timestamp": int(time() * 1000),
        "type": "USER_LOGOUT",
    }


def fake_post():
    return blog.Post(
        **{
            "id": uuid.uuid4(),
            "title": fake.sentence(1),
            "body": fake.sentence(10),
            "user": blog.User(**{"name": fake.word()}),
            "createdAt": int(time() * 1000),
            "updatedAt": int(time() * 1000),
            "timestamp": int(time() * 1000),
        }
    )


def fake_posts():
    return [fake_post() for _ in range(random.randint(10, 50))]


class TodosFetchService(BaseContract):
    def perform(self):
        return generate_todos_week()
