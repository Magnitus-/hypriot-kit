import os, json, sys

from base_image import BaseImage
from root_fs import RootFs
from blank_image import BlankImage
from rpi_bootloader import RpiBootloader
from rpi_kernel import RpiKernel
from rpi_sd_image import RpiSdImage

from output import show

ARTIFACTS = (
    ('base_image', BaseImage),
    ('root_fs', RootFs),
    ('blank_image', BlankImage),
    ('rpi_bootloader', RpiBootloader),
    ('rpi_kernel', RpiKernel),
    ('rpi_sd_image', RpiSdImage))

def get_configs():
    with open(os.path.join(os.getcwd(), 'configs.json'), 'r') as configs_file:
        default_config = json.loads(configs_file.read())
    return default_config

if __name__ == "__main__":
    configs = get_configs()
    for artifact in ARTIFACTS:
        if artifact[0] in configs:
            build_inst = artifact[1](configs)

            show('*************************************************', 'info')
            show('Building component: ' + build_inst.get_description(), 'info')
            show('*************************************************', 'info')

            if not build_inst.is_built():
                build_inst.build()

            show('\n', 'info')
