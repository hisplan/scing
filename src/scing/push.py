import os
from docker.helper import Docker
from docker.aws_ecr import AwsEcr
from docker.quay_io import QuayIO
from scing.error import raise_error


def handle_push(image: str):

    registry, image_name, image_version = Docker.parse_name(image)

    exit_code = Docker.tag(registry, image_name, image_version)
    if exit_code != 0:
        raise_error("Unable to create a docker image tag!")

    # amazon ecr: repo must exist first, so let's create one
    if AwsEcr.is_amazon_ecr(registry):
        if AwsEcr.exists_repos(image_name) != 0:
            exit_code = AwsEcr.create_repos(image_name)
            if exit_code != 0:
                raise_error("Unable to create a repository in AWS ECR!")

    # quay.io: private repo gets created when pushing, so let's manually create a public repo
    elif QuayIO.is_quay_io(registry):
        token = os.environ.get("QUAY_AUTH_TOKEN")
        quay_api = QuayIO(token=token)
        namespace = registry.split("/")[1]
        status_code = quay_api.get_repo(namespace, image_name)
        if status_code == 404:
            # not found, let's create one
            status_code = quay_api.create_repo(namespace, image_name, public=True)
            if status_code == 200 or status_code == 201:
                # successful
                pass
            else:
                raise_error("Unable to create a repo in Red Hat quay.io!")

    exit_code = Docker.push(registry, image_name, image_version)
    if exit_code != 0:
        raise_error("Unable to push an image to docker registry!")

    # quay.io: in case of image pushed to private repo, so let's change to public repo
    if QuayIO.is_quay_io(registry):
        token = os.environ.get("QUAY_AUTH_TOKEN")
        quay_api = QuayIO(token=token)
        namespace = registry.split("/")[1]
        status_code = quay_api.change_visibility(
            namespace=namespace, repo_name=image_name, public=True
        )
        if status_code == 200 or status_code == 201:
            # successful
            pass
        elif status_code == 400:
            # probably the repository already exists. we can ignore this error
            pass
        elif status_code == 403:
            raise_error("Invalid or missing QUAY_AUTH_TOKEN...")
