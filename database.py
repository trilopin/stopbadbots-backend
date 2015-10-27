import aerospike as ae


config = {
    'hosts': [('127.0.0.1', 3000)]
}
aerospike = ae.client(config).connect()