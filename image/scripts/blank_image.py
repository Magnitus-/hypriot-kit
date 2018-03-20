import glob, os

import docker

from builder import BuilderBase

class BlankImage(BuilderBase):
    repo = 'blank_image'

    artifact_pattern = "{device}-raw.img.zip"
    artifact_checksum_pattern = "{device}-raw.img.zip.sha256"

    def get_description(self):
        return "Blank SD Image"

    def __init__(self, configs):
        self.image = configs['blank_image']['image']
        self.repo = configs['blank_image']['repo']
        self.device = configs['blank_image']['device']

    def get_artifacts_names(self):
        return [
            BlankImage.artifact_pattern.format(**{
                "device": self.device
            }),
            BlankImage.artifact_checksum_pattern.format(**{
                "device": self.device
            }),
        ]

    def build_artifacts(self):
        args = {
            "remove": True,
            "privileged": True,
            "volumes": {
                os.environ.get('HYPRIOT_ARTIFACTS_VOLUME'): {
                    "bind": "/workspace"
                }
            },
            "image": self.image
        }

        if self.device == "rpi":
            args['command'] = "/builder/rpi/build.sh"
        elif self.device == "odroid":
            args['command'] = "/builder/odroid/build.sh"

        client = docker.from_env()
        client.containers.run(**args)
