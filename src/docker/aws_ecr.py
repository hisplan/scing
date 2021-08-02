import re
from scing.run_cmd import run_command2


class AwsEcr:
    @staticmethod
    def exists_repos(image_name: str):

        cmd = ["aws", "ecr", "describe-repositories", "--repository-name", image_name]

        exit_code = run_command2(cmd)

        return exit_code

    @staticmethod
    def create_repos(image_name: str):

        cmd = ["aws", "ecr", "create-repository", "--repository-name", image_name]

        exit_code = run_command2(cmd)

        return exit_code

    @staticmethod
    def is_amazon_ecr(registry: str):

        match = re.match(r"(.*)\.dkr\.ecr\.(.*)\.amazonaws.com", registry)

        return True if match else False
