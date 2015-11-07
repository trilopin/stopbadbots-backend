import sys
import os
from settings import settings
from tasks import *
from model.project import Project
from model.persistence import AerospikeSession
sys.path.append(os.path.abspath('.'))

session = AerospikeSession(**settings['aerospike'])
project = session.query(Project).filter_by(full_name='jmpeso/my_project').first()
simple_stats(project=project, interval=720)
#outlier_detector(project=project, interval=30)
