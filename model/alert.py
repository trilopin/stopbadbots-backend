from schematics.types import StringType, IntType, UUIDType
from model import SbbModel
import uuid
import time

class Alert(SbbModel):
    alert_id = UUIDType(required=True, default=uuid.uuid4)
    title = StringType(required=True)
    description = StringType(required=True)
    severity = StringType(required=True)
    user = StringType(partition_key=True)
    project = StringType(required=True)
    created_ts = IntType(required=True, default=time.time)
