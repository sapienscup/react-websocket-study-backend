from cassandra.cqlengine.models import columns
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.usertype import UserType

from src.infra.cass.models.base import BaseModel
from src.infra.middleware.cass import cassandra_middleware
from src.services.todos.fetch import fake


class User(UserType):
    name = columns.Text()
    password = columns.Text()

    __keyspace__ = "blog"


class Post(BaseModel):
    title = columns.Text()
    body = columns.Text()
    user = columns.UserDefinedType(User)

    __keyspace__ = "blog"
    __table_name__ = "posts"


@cassandra_middleware
def create_posts():
    sync_table(Post)

    for _ in range(10):
        Post.create(title=fake.word(), body=fake.sentence(5), user=User(name=fake.name(), password=fake.word()))

create_posts()
