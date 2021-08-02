import os
import sys
import re
import subprocess
import logging
import argparse
from docker.helper import Docker
from scing.build import handle_build
from scing.push import handle_push

logger = logging.getLogger()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("scing.log"), logging.StreamHandler(sys.stdout)],
)


def parse_arguments():

    parser = argparse.ArgumentParser()

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

    parser_build = subparsers.add_parser("build", help="build docker containers")

    parser_build.add_argument(
        "--config",
        action="store",
        dest="path_build_config",
        help="build configuration",
        default="build.yaml",
    )

    # parse arguments
    params = parser.parse_args()

    return params


def main():

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

    if params.command == "push":
        handle_push(params.image)
    elif params.command == "build":
        path_build_config = params.path_build_config
        git_auth_token = os.environ["GIT_AUTH_TOKEN"]
        handle_build(path_build_config, git_auth_token)

    logger.info("DONE.")


if __name__ == "__main__":
    main()
