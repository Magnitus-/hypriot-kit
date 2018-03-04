import glob, os, shutil

import docker

from git_repo import clone

class RootFs(object):
    target_properties = {
        "amd64": {
            "BUILD_ARCH": "amd64"
        },
        "i386": {
            "BUILD_ARCH": "i386"
        },
        "arm64-debian": {
            "BUILD_ARCH": "arm64",
            "QEMU_ARCH": "aarch64"
        },
        "armhf-debian": {
            "BUILD_ARCH": "armhf",
            "QEMU_ARCH": "arm"
        },
        "armhf-raspbian": {
            "BUILD_ARCH": "armhf",
            "QEMU_ARCH": "arm",
            "VARIANT": "raspbian"
        },
        "mips": {
            "BUILD_ARCH": "mips",
            "QEMU_ARCH": "mips"
        }
    }

    def __init__(self, configs):
        self.image = configs['root_fs']['image']
        self.repo = configs['root_fs']['repo']
        self.target = configs['root_fs']['target']
        self.hostname = configs['root_fs']['hostname']
        self.groupname = configs['root_fs']['groupname']
        self.username = configs['root_fs']['username']
        self.password = configs['root_fs']['password']
        self.version = configs['root_fs']['version']

    def image_is_built(self):
        try:
            client = docker.from_env()
            image = client.images.get(self.image)
            return True
        except docker.errors.ImageNotFound:
            return False

    def artifact_is_built(self):
        artifact_matches = glob.glob(os.path.join(os.environ.get('HYPRIOT_ARTIFACTS_VOLUME_PATH'), 'rootfs-*.tar.gz'))
        if len(artifact_matches) > 0:
            return True
        return False

    def is_built(self):
        return self.image_is_built() and self.artifact_is_built()

    def build_image(self):
        repo_dir = os.path.join(os.environ.get('WORKSPACE'), 'repos', 'root_fs')
        clone(self.repo, repo_dir)
        client = docker.from_env()
        client.images.build(path=repo_dir, tag=self.image)
        shutil.rmtree(repo_dir)

    def build_artifact(self):
        args = {
            "remove": True,
            "privileged": True,
            "volumes": {
                os.environ.get('HYPRIOT_ARTIFACTS_VOLUME'): {
                    "bind": "/workspace"
                }
            },
            "environment": {
                "HYPRIOT_HOSTNAME": self.hostname,
                "HYPRIOT_GROUPNAME": self.groupname,
                "HYPRIOT_USERNAME": self.username,
                "HYPRIOT_PASSWORD": self.password,
                "HYPRIOT_OS_VERSION": self.version
            },
            "image": self.image
        }

        for key in RootFs.target_properties[self.target]:
            args['environment'][key] = RootFs.target_properties[self.target][key]

        client = docker.from_env()
        client.containers.run(**args)

    def build(self):
        if not self.image_is_built():
            self.build_image()
        if not self.artifact_is_built():
            self.build_artifact()
