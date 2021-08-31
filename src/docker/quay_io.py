import os
import json
import requests
from requests.exceptions import HTTPError

# document: https://access.redhat.com/documentation/en-us/red_hat_quay/3/html/red_hat_quay_api_guide/using_the_red_hat_quay_api
QUAY_API_URL = "https://quay.io/api/v1"


class QuayIO:
    def __init__(self, token):
        self.token = token

    @staticmethod
    def is_quay_io(registry: str):
        return True if registry.startswith("quay.io") else False

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

        endpoint = f"{QUAY_API_URL}/repository"

        parameters = {
            "visibility": "public" if public else "private",
            "namespace": namespace,
            "repository": repo_name,
            "description": f"Container image '{repo_name}'",
        }

        try:
            response = requests.post(
                url=endpoint,
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

    def get_repo(self, namespace: str, repo_name: str):
        # doc: https://access.redhat.com/documentation/en-us/red_hat_quay/3/html/red_hat_quay_api_guide/appendix_a_red_hat_quay_application_programming_interface_api#get_api_v1_repository_repository

        endpoint = f"{QUAY_API_URL}/repository/{namespace}/{repo_name}"

        try:
            response = requests.get(
                url=endpoint,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.token}",
                },
            )
        except HTTPError as err:
            print(err)

        return response.status_code

    def change_visibility(self, namespace: str, repo_name: str, public: bool):
        # doc: https://access.redhat.com/documentation/en-us/red_hat_quay/3/html/red_hat_quay_api_guide/appendix_a_red_hat_quay_application_programming_interface_api#post_api_v1_repository_repository_changevisibility

        endpoint = f"{QUAY_API_URL}/repository/{namespace}/{repo_name}/changevisibility"

        parameters = {
            "visibility": "public" if public else "private",
        }

        try:
            response = requests.post(
                url=endpoint,
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

    def list(self, namespace: str):
        # doc: https://access.redhat.com/documentation/en-us/red_hat_quay/3/html/red_hat_quay_api_guide/appendix_a_red_hat_quay_application_programming_interface_api#get_api_v1_repository

        endpoint = f"{QUAY_API_URL}/repository?namespace={namespace}"

        try:
            response = requests.get(
                url=endpoint,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.token}",
                },
            )
        except HTTPError as err:
            print(err)

        return response

    def delete(self, namespace: str, repo_name: str):
        # doc: https://access.redhat.com/documentation/en-us/red_hat_quay/3/html/red_hat_quay_api_guide/appendix_a_red_hat_quay_application_programming_interface_api#delete_api_v1_repository_repository

        endpoint = f"{QUAY_API_URL}/repository/{namespace}/{repo_name}"

        try:
            response = requests.delete(
                url=endpoint,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.token}",
                },
            )
        except HTTPError as err:
            print(err)

        return response.status_code
