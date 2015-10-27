import aerospike


config = {
    'hosts': [('127.0.0.1', 3000)]
}
client = aerospike.client(config).connect()

sets = [
    ['stopbadbots', 'example'],
    ['stopbadbots', 'articles'],
    ['stopbadbots', 'user'],
    ['stopbadbots', 'project'],
    ['stopbadbots', 'event'],
    ['stopbadbots', 'alert'],
    ['stopbadbots', 'auth'],
]

def remove_record((key, metadata, record)):
    client.remove(key)

for myset in sets:
    print("Removing {0}.{1}".format(myset[0], myset[1]))
    scan = client.scan(*myset)
    scan.foreach(remove_record)

# asinfo -v "set-config:context=namespace;id=stopbadbots;set=jmpeso/citiservi_es/example;set-delete=true;"
