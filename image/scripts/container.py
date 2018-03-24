import os

import docker

from output import show

def run(args):
    verbosity = os.environ.get('VERBOSITY')
    client = docker.from_env()
    if verbosity != 'debug':
        client.containers.run(**args)
    else:
        args['detach'] = True
        container = client.containers.run(**args)
        show('**************Build Output**************', 'debug')
        for line in container.logs(stream=True):
            show(line.strip(), 'debug')
        show('****************************************', 'debug')
