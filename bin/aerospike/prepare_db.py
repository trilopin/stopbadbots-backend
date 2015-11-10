import sys
import os
sys.path.append(os.path.abspath('.'))
from model.persistence import AerospikeSession
from model.user import User
from model.project import Project
from model.example import Example
from settings import settings
import traceback
import time

try:

    session = AerospikeSession(**settings['aerospike'])

    print("Creating indexes..."),
    session.aerospike.index_string_create(settings['aerospike']['namespace'], 'user', 'name', 'idx_name')
    session.aerospike.index_string_create(settings['aerospike']['namespace'], 'user', 'private_token', 'idx_private_token')
    session.aerospike.index_string_create(settings['aerospike']['namespace'], 'auth', 'token', 'idx_token')
    session.aerospike.index_string_create(settings['aerospike']['namespace'], 'project', 'full_name', 'idx_full_name')
    session.aerospike.index_string_create(settings['aerospike']['namespace'], 'project', 'user', 'idx_projectuser')
    session.aerospike.index_string_create(settings['aerospike']['namespace'], 'example', 'p_interval', 'idx_interval')
    session.aerospike.index_string_create(settings['aerospike']['namespace'], 'example', 'ip_address', 'idx_ip')
    print("ok")

    print("Creating user..."),
    user = User({'name': 'jmpeso', 'email': 'mailexample@gmail.com'})
    user.password = user.make_password('1234')
    session.add(user)

    print('ok (auth token for {0} is {1})'.format(user.name, user.private_token))
    assert user.check_password('1234')

    print("Creating project..."),
    project = Project({
        'user': 'jmpeso',
        'name': 'my_project',
        'logformat': 'ApacheCombinedFormat',
        'logdir': '/opt/data/',
        'logpattern': 'myproject-files-*',
        'hosts': [
            'host1.domain.com',
            'host2.domain.com',
            'host3.domain.com',
        ],
        'whitelist': {
            'bingbot': '157.55.0.0/16',
            'bingbot2': '157.57.0.0/16',
            'googlebot': '66.249.0.0/16'
        }
    })
    session.add(project)
    print('ok')

    # example = Example({
    #     'project': 'jmpeso/citiservi_es',
    #     'ip_address': '8.8.8.8',
    #     'interval': 15,
    #     'data_store': project.data_store,
    #     'period': time.time(),
    #     'param1': 1e-43,
    # })
    # session.add(example)
    # example2 = session.query(Example) \
    #                   .get(example.__key__)
    # print(example2.param1)
    # print(example2.period_dt)


except Exception as error:
    print("Exception caugth, {0}".format(error));
    print(traceback.format_exc())






