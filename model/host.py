from schematics.types import StringType, IntType
from model import SbbModel
import time

class Host(SbbModel):
    name = StringType(required=True)
    user = StringType(required=True)
    ipaddress = StringType(required=True)
    created_ts = IntType(required=True, default=time.time)
