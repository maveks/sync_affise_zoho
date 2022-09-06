import json
import time
import requests
from loguru import logger
from requests import exceptions

logger.add(f"sync_crm.log", level="DEBUG")


def get_users_affise():
    headers = {
        'API-Key': # your key,
    }
    auth_link = # your link,

    result = requests.request("GET", auth_link, headers=headers).json()

    return result


def refresh_access_tokens():
    url = "https://accounts.zoho.eu/oauth/v2/token"

    payload = {'client_id': # your client_id,
               'client_secret': # your client_secret,
               'refresh_token': # your refresh_token,
               'grant_type': 'refresh_token'}
    files = [

    ]
    headers = {
        'Cookie': 'your cookies'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files).json()

    token = response['access_token']
    print(response)
    return token


def search_email(email, token):
    print('search mail in crm...')
    url = f"https://www.zohoapis.eu/crm/v3/Leads/search?email={email}"

    payload = ""
    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload).json()
        print(response)
        exist = True
    except exceptions.JSONDecodeError:
        exist = False
    return exist


def send_record(token, country, login, email, traffic_type_clear, top_offers, skype_telegram, status, hear_about_us):
    url = "https://www.zohoapis.eu/crm/v3/Leads"

    payload = json.dumps({
        "data": [
            {
                "Company": login,
                "First_Name": 'Not',
                "Last_Name": 'available',
                "Email": email,
                "Country": country,
                "Traffic_Type": traffic_type_clear,
                "Top_Offers": top_offers,
                "Skype_ID": skype_telegram,
                "Lead_Status": status,
                "Lead_Source": hear_about_us,
                "wizard_connection_path": [
                    "490366000000316001"
                ],
                "Wizard": {
                    "id": "490366000000316001"
                }
            },
        ],
        "trigger": [
        ]
    })
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()
    print(response)


while True:
    # main
    token = refresh_access_tokens()
    result = get_users_affise()

    revert_list = result['partners'][::-1]

    va = 7 # number of search strings per iteration
    for i in range(0, va):

        email = revert_list[i]['email']
        country = revert_list[i]['country']
        traffic_type = revert_list[i]['customFields'][0]['label']
        top_converting = revert_list[i]['customFields'][1]['label']
        top_offers = revert_list[i]['customFields'][2]['label']
        monthly_turnover = revert_list[i]['customFields'][3]['label']
        skype_telegram = revert_list[i]['customFields'][4]['label']
        hear_about_us = revert_list[i]['customFields'][5]['label']
        status = revert_list[i]['status']
        login = revert_list[i]['login']

        # search company name
        if login == '' or ' ':
            login = email

        # format Traffic type
        b = []
        for i in traffic_type:
            a = traffic_type[f'{i}']
            b.append(a)
        traffic_type_clear = ", ".join(b)

        # logging data
        logger.debug(f'{country}, {traffic_type}, {top_converting}, {top_offers}, {monthly_turnover}, {skype_telegram}, {hear_about_us}, {status}, {email}, {login}')

        # search mail in CRM
        if search_email(email, token):
            logger.debug(f'Почта есть в CRM {email}')
        else:
            logger.debug(f'Почты нет в CRM {email}')
            send_record(token, country, login, email, traffic_type_clear, top_offers, skype_telegram, status,
                        hear_about_us)
    # script sleep
    time.sleep(3600)
