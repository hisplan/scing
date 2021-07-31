#!/usr/bin/env python

import os
import sys
import yaml
import subprocess
import re
import logging
import argparse


logger = logging.getLogger()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("build.log"), logging.StreamHandler(sys.stdout)],
)


def raise_error(msg: str):

    logger.error(msg)
    raise Exception(msg)


def run_command(cmd: list, cwd: str = None):

    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd
    )

    stdout, stderr = process.communicate()

    return process.returncode, stdout, stderr


def run_command2(cmd: list, cwd: str = None):
    "run a command and return (stdout, stderr, exit code)"

    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd, shell=False
    )

    for line in iter(process.stdout.readline, b""):
        line = line.decode(sys.stdout.encoding).rstrip() + "\r"
        logger.info(line)

    process.communicate()

    return process.returncode


def run_shell(cmd):
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )

    stdout, stderr = process.communicate()

    stdout = stdout.decode().strip()
    stderr = stderr.decode().strip()

    return process.returncode, stdout, stderr


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


def set_create_amazon_ecr_repo(config: str, create: bool):

    new_config = re.sub(
        r"create_ecr_repo=.*", "create_ecr_repo=" + ("1" if create else "0"), config
    )

    return new_config


def run_build_script(path_build_script: str):

    cmd = ["bash", "build.sh"]

    exit_code = run_command2(cmd, cwd=path_build_script)

    if exit_code != 0:
        raise_error("build.sh failed!")


def run_package_script(path_package_script: str):

    cmd = ["bash", "package.sh"]

    exit_code = run_command2(cmd, cwd=path_package_script)

    if exit_code != 0:
        raise_error("package.sh failed!")

    # skip if package-for-cromwell.sh doesn't exist
    if not os.path.exists(os.path.join(path_package_script, "package-for_cromwell.sh")):
        return

    cmd = ["bash", "package-for-cromwell.sh"]

    exit_code = run_command2(cmd, cwd=path_package_script)

    if exit_code != 0:
        raise_error("package-for-cromwell.sh failed!")


def get_shell_variable(path_config: str, var_name: str) -> str:

    exit_code, value, _ = run_shell(
        f"bash -c 'source {path_config}; echo ${var_name}'",
    )

    if exit_code != 0:
        raise_error(f"Unable to read config={path_config}' var={var_name}...")

    return value


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


def is_amazon_ecr(registry: str):

    match = re.match(r"(.*)\.dkr\.ecr\.(.*)\.amazonaws.com", registry)

    return True if match else False


def is_quay_io(registry: str):

    return True if registry.startswith("quay.io") else False


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

    new_config = set_create_amazon_ecr_repo(
        config=new_config, create=is_amazon_ecr(registry=registry)
    )

    if is_quay_io(registry):
        from quay import Quay

        token = os.environ.get("QUAY_AUTH_TOKEN")

        quay = Quay(token=token)
        namespace = registry.split("/")[1]
        image_name = get_shell_variable(path_config, "image_name")
        if not image_name:
            raise Exception(f"Unable to retrieve image name from {path_config}...")

        status_code = quay.create_repo(
            namespace=namespace, repo_name=image_name, public=True
        )

        if status_code == 201:
            # successful
            pass
        elif status_code == 400:
            # probably the repository already exists. we can ignore this error
            pass
        elif status_code == 403:
            raise Exception("Invalid or missing QUAY_AUTH_TOKEN...")

    write_config(path_config=path_config, config=new_config)

    verify_config(
        path_config=path_config,
        requested_version=image["version"],
        requested_registry=registry,
    )

    run_build_script(path_dest)

    run_package_script(path_dest)


def build_containers(registry: str, images: str, git_auth_token: str):

    for img in images:

        if "skip" in img:
            if img["skip"] == True:
                continue

        build_container(registry=registry, image=img, git_auth_token=git_auth_token)


def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config",
        action="store",
        dest="path_build_config",
        help="build configuration",
        default="build.yaml",
    )

    # parse arguments
    params = parser.parse_args()

    return params


def main(path_build_config, git_auth_token):

    with open(path_build_config, "rt") as fin:

        config = yaml.safe_load(fin)

        build_containers(
            registry=config["containers"]["registry"],
            images=config["containers"]["images"],
            git_auth_token=git_auth_token,
        )


if __name__ == "__main__":

    logo = r"""
Single-Cell pIpeliNe Garden
 ______     ______     __     __   __     ______
/\  ___\   /\  ___\   /\ \   /\ "-.\ \   /\  ___\
\ \___  \  \ \ \____  \ \ \  \ \ \-.  \  \ \ \__ \
 \/\_____\  \ \_____\  \ \_\  \ \_\\"\_\  \ \_____\
  \/_____/   \/_____/   \/_/   \/_/ \/_/   \/_____/

"""

    print(logo)

    params = parse_arguments()

    git_auth_token = os.environ["GIT_AUTH_TOKEN"]

    main(path_build_config=params.path_build_config, git_auth_token=git_auth_token)

    logger.info("DONE.")
