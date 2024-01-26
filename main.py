import requests
import csv
import hashlib
import hmac
import base64
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
from datetime import datetime
from pprint import pprint  # for debugging

load_dotenv()

PUBLIC_KEY = os.getenv("PUBLIC_KEY")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# CHANGE THESE BEFORE RUNNING
PATH_TO_CSV = "MFC.csv"
sandbox_mode = True

NOTIFY_ENDPOINT = "https://myfigurecollection.net/papi.php?mode=notify-availability"


def load_csv_data(csv_file):
    # Load info from CSV into a list of dictionaries
    data = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(dict(row))

    # Debug pprint
    # pprint(data)

    return data


def handle_response(json, mfci):
    if json['status'] == "FAILED":
        error_msg = f"{datetime.now()}: MFCI:{mfci} | ERROR CODE {json['error']}: {json['message']}"
        print(error_msg)
        with open('error.log', 'a') as file:
            file.write(error_msg + '\n')
    else:
        print(json['status'])


def notify_availability(figure_dict):
    """
    Required parameters (POST variables):
    key - Your public key. (STRING)
    jan - JAN code of the item you want users to be notified about (can be empty if "mfci" optional parameter is set). (STRING)
    status - The item is available for preorder (status=1), in stock (status=2) or on sale (status=3). Please note status=0 will remove your comments.(INTEGER:0|1|2|3)
    s - The above parameters signed with your private key. (STRING)

    Optional parameters (POST variables):
    mfci - If no JAN code, you can use MFC item ID. (INTEGER)
    message - Additional message you want to add to your comment (limited to 200 characters). (STRING)
    price - Price of the item at your shop (Ex: ¥5000 → 5000, $19.99 → 1999). (INTEGER)
    currency - Currency. Default value is JPY. (STRING:JPY|USD|EUR)
    sandbox - Run as test if equal 1 (no comments will be posted). Default value is 0. (INTEGER)

    Please note that the parameters must always be sent in the following order: key, jan, status, s, (optional parameters).
    """

    # Required parameters
    params = {
        'key': PUBLIC_KEY,
        'jan': figure_dict['jan'],
        'status': int(figure_dict['status']),
    }

    # Build signature
    req_string = urlencode(params)
    signature = base64.b64encode(
        hmac.new(PRIVATE_KEY.encode('utf-8'), req_string.encode('utf-8'), hashlib.sha256).digest()
    ).decode('utf-8')
    params['s'] = signature

    # Optional parameters (must come after key, jan, status, and s
    if figure_dict['price'] is not None and figure_dict['price'] != '':
        params['price'] = int(float(figure_dict['price']) * 100)
    if figure_dict['message'] is not None and figure_dict['message'] != '':
        params['message'] = figure_dict['message']
    if figure_dict['mfci'] is not None and figure_dict['mfci'] != '':
        params['mfci'] = int(figure_dict['mfci'])
    if figure_dict['currency'] is not None and figure_dict['currency'] != '':
        params['currency'] = figure_dict['currency']
    if sandbox_mode:
        params['sandbox'] = 1

    # Make the request
    response = requests.post(NOTIFY_ENDPOINT, data=params)
    json_obj = response.json()

    # Debug pprint
    # pprint(json_obj)

    handle_response(json_obj, params['mfci'])


csv_data = load_csv_data("MFC.csv")

for item in csv_data:
    notify_availability(item)
