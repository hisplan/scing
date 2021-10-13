import json
import os
from docker.quay_io import QuayIO

token = os.environ.get("QUAY_AUTH_TOKEN", default="")

if not token:
    print("Set QUAY_AUTH_TOKEN.")
    exit(1)

quayIo = QuayIO(token=token)

response = quayIo.list("devtest")

if response.status_code == 200:
    data = json.loads(response.text)
    repositories = data["repositories"]

    for repo in repositories:

        status_code = quayIo.delete("devtest", repo["name"])
        if status_code == 204:
            print(repo["name"], "DELETED")
        else:
            print(repo["name"], status_code)
else:
    print(response.status_code)
    exit(1)
