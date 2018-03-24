# WIP

This is a work in progress.

Missing functionality is outlined below.

TODO:
- Get sd image adaptations merged back to original repo and point to original repo in default config

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

The behavior of the hypriotkit build is influenced by the project configuration.

The default configuration file can be found at the following path in the project: ```image/configs.json```

Here is the breakdown of the configuration fields:

* base_image: Image used as a base to build all the other building images
  * image: Name to give to the base image. Note that if you change this value, you'll have to change the expected base image in all the other build repos that you use.
  * repo: Repo containing the logic to build the image. Can be the official repo (default) or your custom fork of it.
* root_fs: Core root filesystem for your SD image
  * image: Name to give to the build image that will generate the artifact
  * repo: Repo containing logic to build the build image. Can be the official repo (default) or your custom fork of it.
  * target: Source of the core root filesystem. Can be any of the following: arm64-debian, armhf-debian, armhf-raspbian, mips, amd64, i386
  * hostname: Hostname the os will give itself
  * groupname: Default user groupname
  * username: Default user username
  * password: Default user password
  * version: Version tag of the generated filesystem
* blank_image: Placehold blank image containing the partition sizes of the filesystem
  * image: Name to give to the build image that will generate the artifact
  * repo: Repo containing logic to build the build image. Can be the official repo (default) or your custom fork of it.
  * device: Device to taylor the partitions for. Can be one of the following: rpi, odroid
* rpi_bootloader: Bootfiles for the Raspberry Pi
  * image: Name to give to the build image that will generate the artifact
  * repo: Repo containing logic to build the build image. Can be the official repo (default) or your custom fork of it.
  * firmware_repo: Repo containing the bootfiles to archive. Can be the official repo (default) or your custom fork of it.
* rpi_kernel: Raspberry Pi 64 bits kernel
  * image: Name to give to the build image that will generate the artifact
  * repo: Repo containing logic to build the build image. Can be the official repo (default) or your custom fork of it.
  * kernel_repo: Repo to fetch the kernel from. Can be the official repo (default) or your custom fork of it.
  * branch: Branch of the kernel repo to build from (you can vary this to build different versions of the kernel)
* rpi_sd_image: Hypriot OS final SD image for the Raspberry Pi 64 bits
  * image: Name to give to the build image that will generate the artifact
  * repo: Repo containing logic to build the build image. Can be the official repo (default) or your custom fork of it.
  * docker_engine_version: Version of the docker engine that should be included in the image
  * docker_compose_version: Version of docker-compose that should be included in the image
  * docker_machine_version: Version of Docker Machine that should be included in the image
  * version: Version tag to give the image

Any user-provided configuration file (should be a file called **configs.json** in the target directory of the artifacts) will be combined with the default file in the following way:

* Only the components listed in the user configuration file will be built.
* For each component in the user configuration, the values whichever fields are defined in the user configuration file will be used and the values in the default configuration will be used as fallback for the missing fields.

When defining a subset of the components to build, it is helpful to keep the following depedencies in mind:

* root_fs: base_image
* blank_image: base_image
* rpi_bootloader: base_image
* rpi_kernel: base_image
* rpi_sd_image: root_fs, blank_image, rpi_bootloader, rpi_kernel

For example, a user-provided configuration file to only build the blank image for odroid devices would look like this:

```
{
  "base_image": {
  },
  "blank_image": {
    "device": "odroid"
  }
}

```
