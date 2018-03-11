import glob, os

import docker

from builder import BuilderBase

class RpiBootloader(BuilderBase):
    artifact_pattern = "rpi-raw.img.zip"
    artifact_checksum_pattern = "rpi-raw.img.zip.sha256"

    def __init__(self, configs):
        self.image = configs['rpi_bootloader']['image']
        self.repo = configs['rpi_bootloader']['repo']
        self.firmware_repo = configs['rpi_bootloader']['firmware_repo']

    def get_artifacts_names(self):
        return [RpiBootloader.artifact_pattern, RpiBootloader.artifact_checksum_pattern]

    def build_artifacts(self):
        args = {
            "remove": True,
            "privileged": True,
            "volumes": {
                os.environ.get('HYPRIOT_ARTIFACTS_VOLUME'): {
                    "bind": "/builds"
                }
            },
            "environment": {
                "TIMESTAMP_OUTPUT": False,
                "FIRMWARE_REPO": self.firmware_repo
            },
            "image": self.image
        }

        client = docker.from_env()
        client.containers.run(**args)
