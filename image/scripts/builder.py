import os, subprocess, shutil

import docker

from git_repo import clone
from output import show

class BuilderBase(object):
    def image_is_built(self):
        try:
            client = docker.from_env()
            image = client.images.get(self.image)
            show('Build image ' + self.image + ' found. Skipping image build.', 'info')
            return True
        except docker.errors.ImageNotFound:
            return False

    def build_image(self):
        show('Building build image ' + self.image + '.', 'info')
        repo_dir = os.path.join(os.environ.get('WORKSPACE'), 'repos', self.repo)
        clone(self.repo, repo_dir, self.branch)
        client = docker.from_env()
        client.images.build(path=repo_dir, tag=self.image)
        shutil.rmtree(repo_dir)
        show('Done', 'info')

    def artifacts_are_built(self):
        expected_artifacts = self.get_artifacts_names()
        for expected_artifact in expected_artifacts:
            if not os.path.isfile(os.path.join(os.environ.get('HYPRIOT_ARTIFACTS_VOLUME_PATH'), expected_artifact)):
                return False
        show('Artifacts found. Skipping artifacts build.', 'info')
        return True

    def is_built(self):
        return self.image_is_built() and self.artifacts_are_built()

    def build(self):
        if not self.image_is_built():
            self.build_image()

        if not self.artifacts_are_built():
            show('Building artifacts.', 'info')
            self.build_artifacts()
            show('Done', 'info')
