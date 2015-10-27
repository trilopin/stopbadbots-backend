from schematics.types import StringType, IntType, UUIDType
from model import SbbModel
import uuid
import time


class Action(SbbModel):
    action_id = UUIDType(primary_key=True, default=uuid.uuid4)
    user = StringType(partition_key=True)
    project = StringType(required=True)
    created_ts = IntType(required=True, default=time.time)
