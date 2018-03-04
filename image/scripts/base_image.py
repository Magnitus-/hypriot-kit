import os, subprocess, shutil

import docker

from git_repo import clone

class BaseImage(object):
    def __init__(self, configs):
        self.image = configs['base_image']['image']
        self.repo = configs['base_image']['repo']

    def is_built(self):
        try:
            client = docker.from_env()
            image = client.images.get(self.image)
            return True
        except docker.errors.ImageNotFound:
            return False


    def build(self):
        repo_dir = os.path.join(os.environ.get('WORKSPACE'), 'repos', 'base_image')
        clone(self.repo, repo_dir)
        client = docker.from_env()
        client.images.build(path=repo_dir, tag=self.image)
        shutil.rmtree(repo_dir)
