import re
import logging
from scing.utils import run_command2
from scing.error import raise_error


class Docker:
    @staticmethod
    def tag(registry: str, image_name: str, version: str):

        cmd = [
            "docker",
            "image",
            "tag",
            f"{image_name}:{version}",
            f"{registry}/{image_name}:{version}",
        ]

        exit_code = run_command2(cmd)

        return exit_code

    @staticmethod
    def push(registry: str, image_name: str, version: str):

        cmd = [
            "docker",
            "image",
            "push",
            f"{registry}/{image_name}:{version}",
        ]

        exit_code = run_command2(cmd)

        return exit_code

    @staticmethod
    def parse_name(name: str):

        match = re.search(r"^(.*)/(.*):(.*)$", name)
        if not match:
            raise_error("Invalid docker name supplied.")

        registry = match.group(1)
        image_name = match.group(2)
        image_version = match.group(3)

        return registry, image_name, image_version
