

def ip2int(s):
    "Convert dotted IPv4 address to integer."
    return reduce(lambda a, b: a << 8 | b, map(int, s.split(".")))


def int2ip(ip):
    "Convert 32-bit integer to dotted IPv4 address."
    return ".".join(map(lambda n: str(ip >> n & 0xFF), [24, 16, 8, 0]))


