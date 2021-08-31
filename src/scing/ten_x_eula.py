from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin
from scing.config import Config


def get_form_details(form):
    """
    Returns the HTML details of a form, including action, method and list of form controls (inputs, etc)
    https://www.thepythoncode.com/article/extracting-and-submitting-web-page-forms-in-python
    """
    details = {}
    # get the form action (requested URL)
    action = form.attrs.get("action").lower()
    # get the form method (POST, GET, DELETE, etc)
    # if not specified, GET is the default in HTML
    method = form.attrs.get("method", "get").lower()
    # get all form inputs
    inputs = []
    for input_tag in form.find_all("input"):
        # get type of input form control
        input_type = input_tag.attrs.get("type", "text")
        # get name attribute
        input_name = input_tag.attrs.get("name")
        # get the default value of that input tag
        input_value = input_tag.attrs.get("value", "")
        # add everything to that list
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs

    return details


def get_eula(soup):
    eula = soup.find("div", attrs={"class": "eula"})
    eula = eula.get_text()

    eula, third_party_sw = eula.split("|Third Party Software|||")
    eula = eula.replace("\n", "\n\n").strip() + "\n" + third_party_sw.replace("\n", " ")

    return eula


def get_input_text(msg: str):
    while True:
        value = input(msg)
        value = value.strip()
        if len(value) > 0:
            return value


def get_input_yes(msg: str):
    while True:
        value = input(msg)
        value = value.strip()
        if value == "YES":
            return True


def is_form_deprecated(current_form):

    # as of 2021-08-27
    expected_form = {
        "action": "?",
        "method": "post",
        "inputs": [
            {"type": "text", "name": "first_name", "value": ""},
            {"type": "text", "name": "last_name", "value": ""},
            {"type": "text", "name": "email", "value": ""},
            {"type": "text", "name": "company", "value": ""},
            {"type": "text", "name": "postalCode", "value": ""},
            {"type": "checkbox", "name": "agreed", "value": ""},
            {"type": "hidden", "name": "collectionConsent", "value": "Yes"},
        ],
    }

    # fixme: python3 don't have cmp any more
    # if cmp(expected_form, current_form) == 0:
    #     return False

    # all the key in the expected must be present in the current form
    # all the key-value must match
    for key in expected_form:
        if not key in current_form:
            return True
        if expected_form[key] != current_form[key]:
            return True

    # see if there is a new key in the current form but not in the expected
    for key in current_form:
        if not key in expected_form:
            return True

    return False


def get_user_response(form_details):

    data = {}

    # for testing
    # data["first_name"] = "Jaeyoung"
    # data["last_name"] = "Chun"
    # data["email"] = "chunj@mskcc.org"
    # data["company"] = "Memorial Sloan Kettering Cancer Center"
    # data["postalCode"] = "10065"
    # data["agreed"] = True

    data["first_name"] = get_input_text("First Name: ")
    data["last_name"] = get_input_text("Last Name: ")
    data["email"] = get_input_text("Email: ")
    data["company"] = get_input_text("Company: ")
    data["postalCode"] = get_input_text("Postal Code: ")
    data["agreed"] = get_input_yes(
        "I acknowledge and agree to the terms above and in the 10x Privacy Policy (Enter YES): "
    )

    # iterate through all the input tags
    for input_tag in form_details["inputs"]:
        if input_tag["type"] == "hidden":
            # if it's hidden, use the default value
            data[input_tag["name"]] = input_tag["value"]

    return data


def handle_cookie(cookies):
    """
    Find 10x Genomics EULA cookie from the HTTP response and save it to the config file.
    """

    config = Config()

    # [('sw-eula-full', '...')]
    for cookie in cookies.items():
        key, value = cookie
        if key == config.ten_x_eula_cookie_key:
            config.write_10x_eula_cookie(value)
            return True

    return False


def agree_10x_eula(site_url: str):
    # e.g. site_url="https://support.10xgenomics.com/single-cell-gene-expression/software/downloads/latest"

    session = HTMLSession()

    res = session.get(site_url)

    soup = BeautifulSoup(res.html.html, "html.parser")

    # get 10x Genomics End User Software License Agreement
    eula = get_eula(soup)
    with open("10x-Genomics-EULA.txt", "wt") as fout:
        print(eula, file=fout)
        print(eula)

    print(
        """
-------------------------------------------------------------------------------------------------------------
Scroll up and make sure you read `10x Genomics End User Software License Agreement (EULA)`
You can also find the EULA in `10x-Genomics-EULA.txt` in the current directory.

Please provide your information and agree to the 10x Genomics EULA so that you can start using the software.
"""
    )

    # get all forms
    forms = soup.find_all("form")

    if len(forms) != 1:
        print(
            "The 10x Genomics EULA form seems to have changed. Please contact the SCING developer."
        )
        exit(1)

    form = forms[0]

    # get form details
    form_details = get_form_details(form)

    if is_form_deprecated(form_details):
        print(
            "The 10x Genomics EULA form seems to have changed. Please contact the SCING developer."
        )
        exit(1)

    # get user information
    data = get_user_response(form_details)

    # join the url with the action (form request URL)
    url = urljoin(site_url, form_details["action"])

    # submit the form with user supplied information
    if form_details["method"] == "post":
        res = session.post(url, data=data)
    elif form_details["method"] == "get":
        res = session.get(url, params=data)

    # check status code
    if res.status_code != 200:
        print(
            "The form submission failed for some reason. Please contact the SCING developer."
        )
        exit(1)

    # with open("index.html", "wt") as fout:
    #     print(res.content, file=fout)

    # error if no cookie returned
    if len(res.cookies.items()) == 0:
        print(
            "Make sure you entered your information correctly. If you still encounter an issue, please contact the SCING developer."
        )
        exit(1)

    cookie_found = handle_cookie(res.cookies)
    if cookie_found == False:
        print(
            "Make sure you entered your information correctly. If you still encounter an issue, please contact the SCING developer."
        )
        exit(1)

    print("DONE.")
