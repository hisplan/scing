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
from scing.ten_x_eula import agree_10x_eula
import scing.version

logger = logging.getLogger()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("scing.log"), logging.StreamHandler(sys.stdout)],
)

logo = r"""
Single-Cell pIpeliNe Garden
(pronounced as "sing" /siŋ/)
 ______     ______     __     __   __     ______
/\  ___\   /\  ___\   /\ \   /\ "-.\ \   /\  ___\
\ \___  \  \ \ \____  \ \ \  \ \ \-.  \  \ \ \__ \
 \/\_____\  \ \_____\  \ \_\  \ \_\\"\_\  \ \_____\
  \/_____/   \/_____/   \/_/   \/_/ \/_/   \/_____/

"""


def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="{} v{}".format(parser.prog, scing.version.__version__),
    )

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
        dest="path_config",
        help="configuration file (e.g. config.yaml)"
    )

    parser_install = subparsers.add_parser("install", help="Install pipelines")

    parser_install.add_argument(
        "--config",
        action="store",
        dest="path_config",
        help="configuration file (e.g. config.yaml)"
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
        "--site-url", action="store", dest="site_url", help="10x software download URL", required=True
    )

    parser_download.add_argument(
        "--agree-eula",
        action="store_true",
        dest="agree_eula",
        help="Agree to the 10x Genomics End User Software License Agreement",
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
        path_config = params.path_config
        git_auth_token = os.environ["GIT_AUTH_TOKEN"]
        handle_build(path_config, git_auth_token)

    elif params.command == "install":
        path_config = params.path_config
        path_home = params.path_home
        git_auth_token = os.environ["GIT_AUTH_TOKEN"]
        handle_install(path_config, path_home, git_auth_token)

    elif params.command == "download":
        logger.setLevel(logging.CRITICAL + 1)
        if params.agree_eula:
            agree_10x_eula(params.site_url)
        else:
            handle_download(params.site_url)

    logger.info("DONE.")


if __name__ == "__main__":
    main()
