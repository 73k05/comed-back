import requests
from requests.exceptions import HTTPError

from log import writeLog

# fake header to bypass security
headers = {
    "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}


# Send request to gouv
# sending get request and saving the response as response object
# Return -1 if errors data otherwise
def send_get_request(url):
    try:
        writeLog(f"Send Get Request: {url}")  # Python 3.6

        response = requests.get(url, headers=headers)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        writeLog(f"Request HTTP error occurred: {http_err}")
        return -1
    except Exception as err:
        writeLog(f"Request Other error occurred: {err}")
        return -1
    else:
        return response.text


# Send request to gouv
# sending get request and saving the response as response object
# Return -1 if errors data otherwise
def send_post_request(url, params):
    try:
        writeLog(f"Send Post Request: {url}")  # Python 3.6

        response = requests.post(url, data=params, headers=headers)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        writeLog(f"Request HTTP error occurred: {http_err}")
        return -1
    except Exception as err:
        writeLog(f"Request Other error occurred: {err}")
        return -1
    else:
        return response.text
