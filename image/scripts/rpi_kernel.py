import glob, os

import container

from builder import BuilderBase

class RpiKernel(BuilderBase):
    artifact_pattern = "{version}-hypriotos-v8.tar.gz"
    artifact_checksum_pattern = "{version}-hypriotos-v8.tar.gz.sha256"
    artifact_config_pattern = "{version}-hypriotos-v8.config"
    artifact_bootfiles_pattern = "bootfiles.tar.gz"
    artifact_bootfiles_checksum_pattern = "bootfiles.tar.gz.sha256"

    def get_description(self):
        return "Raspberry Pi 64 Bits Kernel"

    def __init__(self, configs):
        self.image = configs['rpi_kernel']['image']
        self.repo = configs['rpi_kernel']['repo']
        self.kernel_repo = configs['rpi_kernel']['kernel_repo']
        self.branch = configs['rpi_kernel']['branch']

    def get_kernel_version(self):
        if not self.image_is_built():
            self.build_image()

        args = {
            "remove": True,
            "privileged": True,
            "environment": {
                "TIMESTAMP_OUTPUT": False,
                "RPI_KERNEL_BRANCH": self.branch,
                "RPI_KERNEL_REPO": self.kernel_repo
            },
            "command": "/get-kernel-version.sh",
            "image": self.image
        }

        client = docker.from_env()
        return client.containers.run(**args).strip()

    def get_artifacts_names(self):
        kernel_version = self.get_kernel_version()

        return [
            RpiKernel.artifact_pattern.format(version=kernel_version),
            RpiKernel.artifact_checksum_pattern.format(version=kernel_version),
            RpiKernel.artifact_config_pattern.format(version=kernel_version),
            RpiKernel.artifact_bootfiles_pattern,
            RpiKernel.artifact_bootfiles_checksum_pattern
        ]

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
                "RPI_KERNEL_BRANCH": self.branch,
                "RPI_KERNEL_REPO": self.kernel_repo
            },
            "image": self.image
        }

        container.run(args)
