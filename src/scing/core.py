import os
import sys
import re
import subprocess
import logging
import argparse
from docker.helper import Docker
from scing.push import handle_push
from scing.build import handle_build
from scing.install import handle_install
from scing.download import handle_download

logger = logging.getLogger()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("scing.log"), logging.StreamHandler(sys.stdout)],
)

logo = r"""
Single-Cell pIpeliNe Garden
 ______     ______     __     __   __     ______
/\  ___\   /\  ___\   /\ \   /\ "-.\ \   /\  ___\
\ \___  \  \ \ \____  \ \ \  \ \ \-.  \  \ \ \__ \
 \/\_____\  \ \_____\  \ \_\  \ \_\\"\_\  \ \_____\
  \/_____/   \/_____/   \/_/   \/_/ \/_/   \/_____/

"""


def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--no-logo",
        dest="show_logo",
        action="store_false",
    )
    parser.set_defaults(show_logo=True)

    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_push = subparsers.add_parser(
        "push",
        help="push a docker image to docker registry (docker hub, amazon ecr, quay.io)",
    )

    parser_push.add_argument(
        "--image",
        action="store",
        dest="image",
        help="{registry}/{name}:{version}",
        required=True,
    )

    parser_build = subparsers.add_parser("build", help="Build docker containers")

    parser_build.add_argument(
        "--config",
        action="store",
        dest="path_build_config",
        help="build configuration",
        default="build.yaml",
    )

    parser_install = subparsers.add_parser("install", help="Install pipelines")

    parser_install.add_argument(
        "--config",
        action="store",
        dest="path_build_config",
        help="build configuration",
        default="build.yaml",
    )

    parser_install.add_argument(
        "--home",
        action="store",
        dest="path_home",
        help="path to the SCING home where the pipelines will be placed",
    )

    parser_download = subparsers.add_parser(
        "download", help="Retrieve 10x software download URL"
    )

    parser_download.add_argument(
        "--site-url", action="store", dest="site_url", help="site URL", required=True
    )

    # parse arguments
    params = parser.parse_args()

    return params


def main():

    params = parse_arguments()

    if params.show_logo:
        print(logo)

    if params.command == "push":
        handle_push(params.image)

    elif params.command == "build":
        path_build_config = params.path_build_config
        git_auth_token = os.environ["GIT_AUTH_TOKEN"]
        handle_build(path_build_config, git_auth_token)

    elif params.command == "install":
        path_build_config = params.path_build_config
        path_home = params.path_home
        git_auth_token = os.environ["GIT_AUTH_TOKEN"]
        handle_install(path_build_config, path_home, git_auth_token)

    elif params.command == "download":
        logger.setLevel(logging.CRITICAL + 1)
        site_url = params.site_url
        handle_download(site_url)

    logger.info("DONE.")


if __name__ == "__main__":
    main()
