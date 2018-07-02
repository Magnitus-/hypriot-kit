import os

import docker

DEFAULT_IMAGE='magnitus/hypriot-kit:1'
DEFAULT_VOLUME='hypriot-artifacts'

def upgrade_image(image=DEFAULT_IMAGE):
    client = docker.from_env()
    client.images.pull(image)

def ensure_image(image=DEFAULT_IMAGE):
    try:
        client = docker.from_env()
        client.images.get(image)
    except docker.errors.ImageNotFound:
        client.images.pull(image)

def ensure_volume(volume=DEFAULT_VOLUME):
    if not volume.startswith('/'):
        try:
            client = docker.from_env()
            client.volumes.get(volume)
        except docker.errors.NotFound:
            client.volumes.create(
                name=volume,
                driver='local',
                labels={"content": "hypriot-os"}
            )

def build(target=None, volume=DEFAULT_VOLUME, image=DEFAULT_IMAGE, verbosity='quiet'):
    volumes = {
        volume: {
            "bind": "/opt/app/artifacts"
        },
        "/var/run/docker.sock": {
            "bind": "/var/run/docker.sock"
        }
    }

    if target is not None:
        user_configs_path = os.path.join(target, 'configs.json')
        if os.path.isfile(user_configs_path):
            volumes[user_configs_path] = {
                "bind": "/opt/app/user/configs.json"
            }

    client = docker.from_env()
    container = client.containers.run(
        image=image,
        remove=True,
        detach=True,
        volumes=volumes,
        environment={
            "HYPRIOT_ARTIFACTS_VOLUME": volume,
            "VERBOSITY": verbosity
        },
        command=["python", "build.py"]
    )
    for line in container.logs(stream=True):
        print line.strip()


def get_volume_content(target, volume=DEFAULT_VOLUME, image=DEFAULT_IMAGE):
    if not volume.startswith('/'):
        client = docker.from_env()
        command = "sh -c 'cp /opt/volume/* /opt/target/  && chown {uid}:{gid} /opt/target/*'"
        client.containers.run(
            image=image,
            remove=True,
            volumes={
                volume: {
                    "bind": "/opt/volume"
                },
                target: {
                    "bind": "/opt/target"
                }
            },
            command=command.format(
                uid=str(os.geteuid()),
                gid=str(os.getegid())
            )
        )

def destroy_volume(volume=DEFAULT_VOLUME):
    if not volume.startswith('/'):
        client = docker.from_env()
        client.volumes.get(volume).remove()
