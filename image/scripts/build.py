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
    default_configs_path = os.path.join(os.getcwd(), 'configs.json')
    user_configs_path = os.path.join('/', 'opt', 'app', 'user', 'configs.json')
    user_configs = None

    with open(default_configs_path, 'r') as configs_file:
        default_configs = json.loads(configs_file.read())

    if os.path.isfile(user_configs_path):
        with open(user_configs_path, 'r') as configs_file:
            user_configs = json.loads(configs_file.read())

    if user_configs is None:
        return default_configs
    else:
        for key in user_configs:
            merged_key = default_configs[key].copy()
            merged_key.update(user_configs[key])
            user_configs[key] = merged_key
        return user_configs

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
