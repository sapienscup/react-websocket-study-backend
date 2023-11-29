from src.contracts.base import BaseContract
from src.infra.cass.models.blog import Post
from src.services.todos.fetch import fake_posts
from src.infra.envs.envs import get_env_mode


class PostService(BaseContract):
    def perform(self):
        return fake_posts() if get_env_mode() == "staging" else Post.all()
