# WIP

This is a work in progress. I'm making the repo public at the present time even though it isn't completed to publish an image on Docker Hub.

Currently, the components for the SD image are generated, but not the final SD image.

Also, the top-level script (to combine user-provided configuration files with the default, create the docker volume where artifacts are stored and provide functionality to move the artifacts in the current directory) is currently missing and a place-holder docker-compose file is currently used in its stead.

TODO:
- Combine SD image components into SD image
- Create installable top-level script that you can install & run like a binary

# Overview

This repo is meant to automatically generate SD images and image artifacts from the Hypriot OS repos.

The aim is to provide as much composability as possible via configuration files and to minimize reliance on pre-generated artifacts as much as possible (the tool attempts to generate everything from the repos) in a package that is as user-friendly as possible given those aims.

My current aim is to compile a 64 bit Raspberry Pi hypriot image. Support for other type of images (ie, Odroid or 32 bits Raspberry) is currently limited to artifacts that have multi-platform repos.

Usability documentation will follow once the work (at least for 64 bit Raspberry Pi) is complete.
