from schematics.types import StringType, IntType, IPv4Type
from model import SbbModel

class IpAddress(SbbModel):
    ipaddress = IPv4Type(primary_key=True)
    status = IntType()
    #history = Map(Integer, Integer)

