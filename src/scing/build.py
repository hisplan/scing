#!/usr/bin/env python

import os
import yaml
import re
import logging
from scing.error import raise_error
from scing.utils import run_command, run_command2, get_shell_variable
from scing.utils import download_from_github, extract_targzip

logger = logging.getLogger()


def read_config(path_config: str):

    with open(path_config, "rt") as fin:
        config = fin.read()

    return config


def write_config(path_config: str, config: str):

    with open(path_config, "wt") as fout:
        fout.write(config)
        fout.write("\n")


def set_docker_registry(config: str, registry: str):

    new_config = re.sub(r"registry=\"(.*)\"", f'registry="{registry}"', config)

    return new_config


def run_build_script(path_build_script: str):

    cmd = ["bash", "build.sh"]

    exit_code = run_command2(cmd, cwd=path_build_script)

    if exit_code != 0:
        raise_error("build.sh failed!")


def run_push_script(path_push_script: str):

    cmd = ["bash", "push.sh"]

    exit_code = run_command2(cmd, cwd=path_push_script)

    if exit_code != 0:
        raise_error("push.sh failed!")


def verify_config(path_config: str, requested_version: str, requested_registry: str):

    # verify version
    actual_version = get_shell_variable(path_config, "version")

    if actual_version != requested_version:
        raise_error(
            f"Actual version {actual_version} != Requested version {requested_version}"
        )

    # verify container registry
    actual_registry = get_shell_variable(path_config, "registry")

    if actual_version != requested_version:
        raise_error(
            f"Actual registry {actual_registry} != Requested registry {requested_registry}"
        )


def build_container(registry: str, image: dict, git_auth_token: str):

    # convert to string so that we can compare later against config.sh
    image["version"] = str(image["version"])

    logger.info("Building {}/{}:{}".format(registry, image["name"], image["version"]))

    path_base_dest = "workspace/containers"

    path_dest = download_from_github(
        name=image["name"],
        version=image["version"],
        download_url=image["download_url"],
        path_base_dest=path_base_dest,
        git_auth_token=git_auth_token,
    )

    path_dest = extract_targzip(
        name=image["name"],
        version=image["version"],
        targzip=path_dest,
        path_base_dest=path_base_dest,
    )

    # use subdirectory if necessary
    if "directory" in image:
        if image["directory"]:
            path_dest = os.path.join(path_dest, image["directory"])

    logger.info(f"Working Directory: {path_dest}")

    path_config = os.path.join(path_dest, "config.sh")

    config = read_config(path_config=path_config)

    new_config = set_docker_registry(config=config, registry=registry)

    write_config(path_config=path_config, config=new_config)

    verify_config(
        path_config=path_config,
        requested_version=image["version"],
        requested_registry=registry,
    )

    run_build_script(path_dest)

    run_push_script(path_dest)


def build_containers(registry: str, images: list, git_auth_token: str):

    for img in images:

        if "skip" in img:
            if img["skip"] == True:
                continue

        build_container(registry=registry, image=img, git_auth_token=git_auth_token)


def handle_build(path_build_config, git_auth_token):

    with open(path_build_config, "rt") as fin:

        config = yaml.safe_load(fin)

        build_containers(
            registry=config["containers"]["registry"],
            images=config["containers"]["images"],
            git_auth_token=git_auth_token,
        )
