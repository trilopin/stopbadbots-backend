from schematics.types import StringType, IntType, UUIDType
from model import SbbModel
import uuid
import time

class Event(SbbModel):
    event_id = UUIDType(required=True, default=uuid.uuid4)
    created_ts = IntType(required=True, default=time.time)
    user = StringType(required=True)
    project = StringType(required=True)
    title = StringType(required=True)
    description = StringType(required=True)
    event_type = StringType(required=True)
    reference = StringType()
