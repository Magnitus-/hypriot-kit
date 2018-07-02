import glob, os

import container

from builder import BuilderBase

class RpiBootloader(BuilderBase):
    artifact_pattern = "rpi-bootloader.tar.gz"
    artifact_checksum_pattern = "rpi-bootloader.tar.gz.sha256"

    def get_description(self):
        return "Raspberry Pi Bootloader"

    def __init__(self, configs):
        self.image = configs['rpi_bootloader']['image']
        self.repo = configs['rpi_bootloader']['repo']
        self.branch = configs['rpi_bootloader'].get('branch')
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
                "TIMESTAMP_OUTPUT": "false",
                "FIRMWARE_REPO": self.firmware_repo
            },
            "image": self.image
        }

        container.run(args)
