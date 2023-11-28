from src.contracts.base import BaseContract
from src.infra.cass.models.blog import Post
from src.services.todos.fetch import fake_posts

class PostService(BaseContract):
    def perform(self):
        try:
            return Post.all()
        except Exception:
            return fake_posts()
