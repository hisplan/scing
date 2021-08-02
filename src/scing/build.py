#!/usr/bin/env python

import os
import sys
import yaml
import subprocess
import re
import logging
import argparse
from docker.aws_ecr import AwsEcr
from docker.quay_io import QuayIO
from scing.error import raise_error
from scing.run_cmd import run_command, run_command2, get_shell_variable

logger = logging.getLogger()


def download_from_github(
    name: str,
    version: str,
    download_url: str,
    git_auth_token: str,
    skip_exists: bool = True,
):

    os.makedirs("workspace/containers", exist_ok=True)

    path_dest = f"workspace/containers/{name}-{version}.tgz"

    # skip if file exists and skip_exists=true
    if os.path.exists(path_dest) and skip_exists == True:
        return path_dest

    cmd = [
        "curl",
        "-L",
        "-o",
        path_dest,
        "-H",
        f"Authorization: token {git_auth_token}",
        download_url,
    ]

    logger.info(" ".join(cmd))

    exit_code = run_command2(cmd)

    if exit_code != 0:
        raise_error("curl failed!")

    return path_dest


def extract_targzip(name: str, version: str, targzip: str):

    path_dest = f"workspace/containers/{name}-{version}"

    os.makedirs(path_dest, exist_ok=True)

    cmd = ["tar", "xzf", targzip, "-C", path_dest, "--strip-components", "1"]

    exit_code, stdout, stderr = run_command(cmd)

    if exit_code != 0:
        raise_error("tar xzf failed!")

    stdout = stdout.decode()
    stderr = stderr.decode()

    if stdout:
        logger.info(stdout)

    if stderr:
        logger.error(stderr)

    return path_dest


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


# def set_create_amazon_ecr_repo(config: str, create: bool):

#     new_config = re.sub(
#         r"create_ecr_repo=.*", "create_ecr_repo=" + ("1" if create else "0"), config
#     )

#     return new_config


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


def build_container(registry: str, image: str, git_auth_token: str):

    # convert to string so that we can compare later against config.sh
    image["version"] = str(image["version"])

    logger.info("Building {}/{}:{}".format(registry, image["name"], image["version"]))

    path_dest = download_from_github(
        name=image["name"],
        version=image["version"],
        download_url=image["download_url"],
        git_auth_token=git_auth_token,
    )

    path_dest = extract_targzip(
        name=image["name"], version=image["version"], targzip=path_dest
    )

    # use subdirectory if necessary
    if "directory" in image:
        if image["directory"]:
            path_dest = os.path.join(path_dest, image["directory"])

    logger.info(f"Working Directory: {path_dest}")

    path_config = os.path.join(path_dest, "config.sh")

    config = read_config(path_config=path_config)

    new_config = set_docker_registry(config=config, registry=registry)

    # new_config = set_create_amazon_ecr_repo(
    #     config=new_config, create=AwsEcr.is_amazon_ecr(registry=registry)
    # )

    write_config(path_config=path_config, config=new_config)

    verify_config(
        path_config=path_config,
        requested_version=image["version"],
        requested_registry=registry,
    )

    run_build_script(path_dest)

    run_push_script(path_dest)


def build_containers(registry: str, images: str, git_auth_token: str):

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
