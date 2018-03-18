# WIP

This is a work in progress. I'm making the repo public at the present time even though it isn't completed to publish an image on Docker Hub.

While the binary to run the project in a more user-friendly way is completed, the logic to combine user-provided configurations with the default configuration baked into the image is not yet implemented.

TODO:
- Add logic to merge user-provided configuration into the default
- Add optional verbosity (nice to have)
- Add option to use mapped volume instead of named volume for artifacts (nice to have)

# Overview

This repo is meant to automatically generate SD images and image artifacts from the Hypriot OS repos.

The aim is to provide as much composability as possible via configuration files and to minimize reliance on pre-generated artifacts as much as possible (the tool attempts to generate everything from the repos) in a package that is as user-friendly as possible given those aims.

My current aim is to compile a 64 bit Raspberry Pi hypriot image. Support for other type of images (ie, Odroid or 32 bits Raspberry) is currently limited to artifacts that have multi-platform repos.

# Compatibility

You will need Python 2, the [Docker Python Package](https://github.com/docker/docker-py), Docker, docker-machine, Virtualbox and I think that's about it.

This script is being developped on a Ubuntu 16.04 machine and should work on any Linux machines that have a kernel recent enough to run Docker.

It should also theoretically work on a Mac, but being Macless and not deeply versed on the status of Mac compatibility, it's hard for me to say until someone with a Mac runs it and tells me it works.

# Usage

This project comes with 3 components:
- Image logic to orchestrate the Hypriot repos to build Hypriot OS components in a user-friendly and composable way
- An API library to make user of the above image in a way that is more user-friendly
- A binary to make use of the above API library in a way that is more user-friendly

## Installation

Run ```python setup.py install```

If you get this error while using the binary or API:

```
chroot: failed to run command '/debootstrap/debootstrap': Exec format error
```

Type the following and run the script again:

```
sudo modprobe binfmt_misc
```

## The API

The library is called **hypriotkitapi**.

```
upgrade_image(image='magnitus/hypriot-kit:latest')
```

Pull the latest build image. You can change the image name to one that you control.

```
ensure_image(image='magnitus/hypriot-kit:latest')
```

Pull the latest build image if it is not present on your machine.

You can change the image name to one that you control.

```
ensure_volume(volume='hypriot-artifacts')
```

Creates the volume to cache Hypriot artifacts if it is not present on your machine.

Here, you can change the expected volume name, potentially to avoid name clashes or cache different artifacts for different builds.

```
build(target=None, volume='hypriot-artifacts', image='magnitus/hypriot-kit:latest')
```

Builds the Hypriot OS artifacts in the Docker cache volume. If a 'configuration.json' file is present in the 'target' directory, it will be merged with the default configuration.

As before, you can also change the expected build image name and volume name in the options.

```
get_volume_content(target, volume='hypriot-artifacts', image='magnitus/hypriot-kit:latest')
```

Copy the Hypriot artifacts built into the Docker cache volume to 'target'.

As before, you can also change the expected build image name and volume name in the options.

```
destroy_volume(volume='hypriot-artifacts')
```

Destroy the Docker cache volume.

As before, you can also change the expected volume name in the options.

## The binary

The binary is simply **hypriotkit** and can be executed on the shell after installation.

It has the following build options:

* target: Target directory where the artifacts should be copied to. If a **configuration.json** file is present in that directory, it will be merged with the default configurations.
* image: Build image to pull if not present. Defaults to 'magnitus/hypriot-kit:latest'.
* volume: Cache volume name to store Hypriot artifacts in. Defaults to 'hypriot-artifacts'.
* cmd:
  * build: build the artifacts
  * clean: delete the Docker cache volume
  * upgrade: pull the latest build image from the registry

For help, you can type:

```
hypriotkit --help
```

## Configuration format

TODO
