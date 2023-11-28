import time
import uuid

from cassandra.cqlengine.models import Model, columns


class BaseModel(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    created_at = columns.Text(default=f"{int(time.time() * 1000)}")
    updated_at = columns.Text(default=f"{int(time.time() * 1000)}")
