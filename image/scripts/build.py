import os, json, sys

from base_image import BaseImage
from root_fs import RootFs
from blank_image import BlankImage

ARTIFACTS = (('base_image', BaseImage), ('root_fs', RootFs), ('blank_image', BlankImage))

def get_configs():
    with open(os.path.join(os.getcwd(), 'configs.json'), 'r') as configs_file:
        return json.loads(configs_file.read())

if __name__ == "__main__":
    configs = get_configs()
    for artifact in ARTIFACTS:
        if artifact[0] in configs:
            build_inst = artifact[1](configs)
            if not build_inst.is_built():
                build_inst.build()
