import os

import docker

def ensure_image(image='magnitus/hypriot-kit:latest'):
    try:
        client = docker.from_env()
        client.images.get(image)
    except docker.errors.ImageNotFound:
        client.images.pull(image)

def ensure_volume(volume='hypriot-artifacts'):
    try:
        client = docker.from_env()
        client.volumes.get(volume)
    except docker.errors.NotFound:
        client.volumes.create(
            name=volume,
            driver='local',
            labels={"content": "hypriot-os"}
        )

def build(target=None, volume='hypriot-artifacts', image='magnitus/hypriot-kit:latest'):
    volumes = {
        volume: {
            "bind": "/opt/app/artifacts"
        },
        "/var/run/docker.sock": {
            "bind": "/var/run/docker.sock"
        }
    }

    if target is not None and os.path.isfile(user_configs_path):
        user_configs_path = os.path.join(target, 'configs.json')
        volumes[user_configs_path] = "/opt/app/user/configs.json"

    client = docker.from_env()
    client.containers.run(
        image=image,
        remove=True,
        volumes=volumes,
        command=["python", "build.py"]
    )


def get_volume_content(target, volume='hypriot-artifacts', image='magnitus/hypriot-kit:latest'):
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

def destroy_volume(volume='hypriot-artifacts'):
    client = docker.from_env()
    client.volumes.get(volume).remove()
