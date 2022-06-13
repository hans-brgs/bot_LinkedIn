from time import sleep
import requests
from selenium import webdriver
from utils.ft_file_handle import log_error, log_response
import utils.ft_settings as ft_settings

def get_token_state(client_id, client_secret, access_token):

    URL = "https://www.linkedin.com/oauth/v2/introspectToken"

    # request's ARGS
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    token_expiration = "client_id=" + client_id + \
        "&client_secret=" + client_secret + "&token=" + access_token

    # POST request
    response = requests.post(URL, headers=headers, data=token_expiration)
    log_response("TOKEN_STATE_RESPONSE : ", response)
    if response.status_code != 200:
        return "error", 0
    response = response.json()

    # response's variables
    create_at = response["created_at"]
    expire_at = response["expires_at"]
    day_left = round((expire_at - create_at)/86400)
    status = response["status"]

    return day_left, status


def get_code_authorization(client_id, redirect_url):

    URL = 'https://www.linkedin.com/oauth/v2/authorization'

    # request's ARGS
    state = "complete"
    URL = (URL +
           "?response_type=code" +
           "&client_id=" + client_id +
           "&redirect_uri=" + redirect_url +
           "&state=" + state +
           "&scope=w_member_social,r_liteprofile")

    # Launch Google Chrome : Sign in to LinkedIn
    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver")
    driver.get(URL)
    while True:
        get_url = driver.current_url
        if "code=" in get_url:
            break
        sleep(1)
    driver.close()

    # Get The OAuth 2.0 authorization code in the URL
    OAuth_code = get_url.split("?code=")[1].split("&state=")[0]
    return_state = get_url.split("&state=")[1]

    # Compare state, if not match, possible CSRF ATTACKS
    if return_state != state:
        log_error("ERROR_CODE_AUTHORIZATION : POSSIBLE CSRF ATTACKS")
        return
    else:
        return (OAuth_code)


def get_acces_token(OAuth_code, redirect_url, client_id, client_secret):

    URL = 'http://www.linkedin.com/oauth/v2/accessToken'

    # request's ARGS
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = ("grant_type=authorization_code" +
            "&code=" + OAuth_code +
            "&redirect_uri=" + redirect_url +
            "&client_id=" + client_id +
            "&client_secret=" + client_secret)

    # POST request
    response = requests.post(URL, headers=headers, data=data)
    log_response("TOKEN_ACCESS_RESPONSE : ",response)
    if response.status_code != 200:
        return
    response = response.json()
    access_token = response["access_token"]

    # Write token in a file
    f = open(ft_settings.token_file, "w")
    f.write(access_token)
    f.close()
    return access_token
