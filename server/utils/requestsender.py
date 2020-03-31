from log import writeLog
import requests
from requests.exceptions import HTTPError


# fake header to bypass security
headers = {
    "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

# Send request to gouv
# sending get request and saving the response as response object
# Return -1 if errors data otherwise
def sendGetRequest(url):
    try:
        writeLog(f"\r\nSend Get Request: {url}\r\n")  # Python 3.6

        response = requests.get(url, headers=headers)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        writeLog(f"\r\nRequest HTTP error occurred: {http_err}\r\n")
        return -1
    except Exception as err:
        writeLog(f"\r\nRequest Other error occurred: {err}\r\n")
        return -1
    else:
        return response.text