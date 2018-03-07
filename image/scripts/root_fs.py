import glob, os

import docker

from builder import BuilderBase

class RootFs(BuilderBase):
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

    repo = 'root_fs'
    artifact_pattern = 'rootfs-{target}-{version}.tar.gz'

    def __init__(self, configs):
        self.image = configs['root_fs']['image']
        self.repo = configs['root_fs']['repo']
        self.target = configs['root_fs']['target']
        self.hostname = configs['root_fs']['hostname']
        self.groupname = configs['root_fs']['groupname']
        self.username = configs['root_fs']['username']
        self.password = configs['root_fs']['password']
        self.version = configs['root_fs']['version']


    def get_artifacts_names(self):
        return [RootFs.artifact_pattern.format(**{
            "target": self.target,
            "version": self.version
        })]

    def build_artifacts(self):
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
