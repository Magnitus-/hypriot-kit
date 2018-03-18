import glob, os

import docker

from root_fs import RootFs
from blank_image import BlankImage
from rpi_bootloader import RpiBootloader
from rpi_kernel import RpiKernel

from builder import BuilderBase

class RpiSdImage(BuilderBase):
    artifact_pattern = "hypriotos-rpi64-{version}.img.zip"
    artifact_checksum_pattern = "hypriotos-rpi64-{version}.img.zip.sha256"

    def __init__(self, configs):
        self.image = configs['rpi_sd_image']['image']
        self.repo = configs['rpi_sd_image']['repo']
        self.docker_engine_version = configs['rpi_sd_image']['docker_engine_version']
        self.docker_compose_version = configs['rpi_sd_image']['docker_compose_version']
        self.docker_machine_version = configs['rpi_sd_image']['docker_machine_version']
        self.version = configs['rpi_sd_image']['version']
        self.configs = configs

    def get_artifacts_names(self):
        return [
            RpiKernel.artifact_pattern.format(version=self.version),
            RpiKernel.artifact_checksum_pattern.format(version=self.version)
        ]

    def build_artifacts(self):
        root_fs_instance = RootFs(self.configs)
        blank_image_instance = BlankImage(self.configs)
        rpi_bootloader_instance = RpiBootloader(self.configs)
        rpi_kernel_instance = RpiKernel(self.configs)

        args = {
            "remove": True,
            "privileged": True,
            "volumes": {
                os.environ.get('HYPRIOT_ARTIFACTS_VOLUME'): {
                    "bind": "/workspace"
                },
                "/boot": {
                    "bind": "/boot"
                },
                "/lib/modules": {
                    "bind": "/lib/modules"
                }
            },
            "environment": {
                "FETCH_MISSING_ARTIFACTS": "false",
                "DOCKER_ENGINE_VERSION": self.docker_engine_version,
                "DOCKER_COMPOSE_VERSION": self.docker_compose_version,
                "DOCKER_MACHINE_VERSION": self.docker_machine_version,
                "KERNEL_VERSION": rpi_kernel_instance.get_kernel_version(),
                "BOOTLOADER_ARTIFACT": rpi_bootloader_instance.get_artifacts_names()[0],
                "RAW_IMAGE_ARTIFACT": blank_image_instance.get_artifacts_names()[0],
                "ROOT_FS_ARTIFACT": root_fs_instance.get_artifacts_names()[0],
                "KERNEL_ARTIFACT": rpi_kernel_instance.get_artifacts_names()[0]
            },
            "image": self.image
        }

        client = docker.from_env()
        return client.containers.run(**args)
