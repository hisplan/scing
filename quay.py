import os
import json
import requests
from requests.exceptions import HTTPError

QUAY_API_URL = "https://quay.io/api/v1/repository"


class Quay:
    def __init__(self, token):

        self.token = token

    def create_repo(self, namespace: str, repo_name: str, public: bool):

        # curl example
        # export namespace="dpeerlab"
        # export container="hey-world"
        # export token="xyz-123-abc"
        # curl -X POST https://quay.io/api/v1/repository \
        #     -d '{"namespace":"'$namespace'","repository":"'$container'","description":"Container image '$container'","visibility":"public"}' \
        #     -H 'Authorization: Bearer '$token'' -H "Content-Type: application/json"

        # if successful
        # {'kind': 'image', 'namespace': 'dpeerlab', 'name': 'hello-world'}

        # if already exists:
        # {'status': 400, 'error_message': 'Repository already exists', 'title': 'invalid_request', 'error_type': 'invalid_request', 'detail': 'Repository already exists', 'type': 'https://quay.io/api/v1/error/invalid_request'}

        parameters = {
            "visibility": "public" if public else "private",
            "namespace": namespace,
            "repository": repo_name,
            "description": f"Container image '{repo_name}'",
        }

        try:
            response = requests.post(
                url=QUAY_API_URL,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.token}",
                },
                json=parameters,
            )
        except HTTPError as err:
            print(err)

        return response.status_code


if __name__ == "__main__":

    token = os.environ.get("QUAY_AUTH_TOKEN")

    quay = Quay(token=token)

    response = quay.create_repo(
        namespace="dpeerlab", repo_name="hello-world", public=True
    )

    print(response)
