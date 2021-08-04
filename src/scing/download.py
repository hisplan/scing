import os
import re
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup


def handle_download(site_url: str):

    try:
        cookies = dict()

        cookies["sw-eula-full"] = os.environ.get("SW_EULA_10x")

        response = requests.get(site_url, cookies=cookies)

        if "Software License Agreement" in response.text:
            print(
                "You must first sign the 10x Genomics End User Software License Agreement:"
            )
            print(site_url)
            exit(1)

        soup = BeautifulSoup(response.text, "html.parser")

        # soup.find_all()
        result = soup.select("div.download-command")

        if len(result) == 0:
            print("Unable to find the download URL.")
            exit(1)

        curl_cmd = result[0].text

        match = re.search(r'"(.*)"', curl_cmd)
        if not match:
            print(curl_cmd)
            print("Unable to retrieve the download URL.")
            exit(1)

        download_url = match.group(1)

        print(download_url)

    except HTTPError as err:
        print(err)
        exit(1)
