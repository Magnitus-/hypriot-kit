import os, subprocess, shutil

import docker

from git_repo import clone

class BuilderBase(object):
    def image_is_built(self):
        try:
            client = docker.from_env()
            image = client.images.get(self.image)
            return True
        except docker.errors.ImageNotFound:
            return False

    def build_image(self):
        repo_dir = os.path.join(os.environ.get('WORKSPACE'), 'repos', self.repo)
        clone(self.repo, repo_dir)
        client = docker.from_env()
        client.images.build(path=repo_dir, tag=self.image)
        shutil.rmtree(repo_dir)

    def artifacts_are_built(self):
        expected_artifacts = self.get_artifacts_names()
        for expected_artifact in expected_artifacts:
            if not os.path.isfile(os.path.join(os.environ.get('HYPRIOT_ARTIFACTS_VOLUME_PATH'), expected_artifact)):
                return False
        return True

    def is_built(self):
        return self.image_is_built() and self.artifacts_are_built()

    def build(self):
        if not self.image_is_built():
            self.build_image()
        if not self.artifacts_are_built():
            self.build_artifacts()
