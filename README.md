# WIP

This is a work in progress.

Missing functionality is outlined below.

TODO:
- Add logic to merge user-provided configuration into the default
- Add output for debug verbosity

# Overview

This repo is meant to automatically generate SD images and image artifacts from the Hypriot OS repos.

The aim is to provide as much composability as possible via configuration files and to minimize reliance on pre-generated artifacts as much as possible (the tool attempts to generate everything from the repos) in a package that is as user-friendly as possible given those aims.

My current aim is to compile a 64 bit Raspberry Pi hypriot image. Support for other type of images (ie, Odroid or 32 bits Raspberry) is currently limited to artifacts that have multi-platform repos.

# Compatibility

You will need Python 2, the [Docker Python Package](https://github.com/docker/docker-py), Docker, docker-machine, Virtualbox and I think that's about it.

This script is being developped on a Ubuntu 16.04 machine and should work on any Linux machines that have a kernel recent enough to run Docker.

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

Creates the Docker volume **volume** to store Hypriot artifacts if it is not present on your machine.

Here, you can change the expected volume name, potentially to avoid name clashes or cache different artifacts for different builds.

If the value of **volume** is a mapped volume, this is a no-op.

```
build(target=None, volume='hypriot-artifacts', image='magnitus/hypriot-kit:latest', verbosity='quiet')
```

Builds the Hypriot OS artifacts in the Docker volume **volume**. If a 'configs.json' file is present in the **target** directory, it will be merged with the default configuration.

Build **verbosity** can be set to 'quiet', 'info' or 'debug'. The first will output only error, the second will output a top-level overview of what is happening and the third will ouput the build containers' output which may be substantial.

As before, you can also change the expected build image name and volume in the options.

```
get_volume_content(target, volume='hypriot-artifacts', image='magnitus/hypriot-kit:latest')
```

Copy the Hypriot artifacts built into **volume** to **target**.

As before, you can also change the expected build image name and volume name in the options.

If the value of **volume** is a mapped volume, this is a no-op.

```
destroy_volume(volume='hypriot-artifacts')
```

Destroy the Docker volume **volume**.

As before, you can also change the expected volume name in the options.

If the value of **volume** is a mapped volume, this is a no-op.

## The binary

The binary is simply **hypriotkit** and can be executed on the shell after installation.

It has the following build options:

* target: Target directory where the artifacts should be copied to. If a **configs.json** file is present in that directory, it will be merged with the default configurations.
* image: Build image to pull if not present. Defaults to 'magnitus/hypriot-kit:latest'.
* volume: Named volume to cache Hypriot artifacts in prior to copying them to **target**. If no value is passed, then a mapped volume to **target** is used directly, bypassing the need for a named caching volume.
* cmd:
  * build: build the artifacts
  * clean: delete the Docker volume if it is a named volume
  * upgrade: pull the latest build image from the registry
* verbosity: Build verbosity. Defaults to 'quiet'. See **build** method of the API for details.

For help, you can type:

```
hypriotkit --help
```

## Configuration format

TODO
