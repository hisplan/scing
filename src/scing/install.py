#!/usr/bin/env python

import yaml
import logging
from scing.error import raise_error
from scing.utils import run_command, run_command2, get_shell_variable
from scing.utils import download_from_github, extract_targzip

logger = logging.getLogger()


def run_make_deployable_script(path_make_deployable_script: str, path_scing_home: str):

    cmd = ["bash", "make-deployable.sh"]

    if path_scing_home:
        cmd.extend(["-d", path_scing_home])

    exit_code, _, _ = run_command(cmd, cwd=path_make_deployable_script)

    if exit_code != 0:
        raise_error("make-deployable.sh failed!")


def install_pipeline(package: dict, path_home: str, git_auth_token: str):

    # convert to string so that we can compare later against config.sh
    package["version"] = str(package["version"])

    logger.info("Building {}:{}".format(package["name"], package["version"]))

    path_base_dest = "workspace/pipelines"

    path_dest = download_from_github(
        name=package["name"],
        version=package["version"],
        download_url=package["download_url"],
        path_base_dest=path_base_dest,
        git_auth_token=git_auth_token,
    )

    path_dest = extract_targzip(
        name=package["name"],
        version=package["version"],
        targzip=path_dest,
        path_base_dest=path_base_dest,
    )

    run_make_deployable_script(path_dest, path_home)


def install_pipelines(packages: list, path_home: str, git_auth_token: str):

    for pkg in packages:

        if "skip" in pkg:
            if pkg["skip"] == True:
                continue

        install_pipeline(
            package=pkg, path_home=path_home, git_auth_token=git_auth_token
        )


def handle_install(path_build_config, path_home, git_auth_token):

    with open(path_build_config, "rt") as fin:

        config = yaml.safe_load(fin)

        install_pipelines(
            packages=config["pipelines"]["packages"],
            path_home=path_home,
            git_auth_token=git_auth_token,
        )
