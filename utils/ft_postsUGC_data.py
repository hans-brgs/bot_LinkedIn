import requests

def find_UGCposts(access_token, profile_id):

    URL = 'https://api.linkedin.com/v2/me?q=authors&authors=List(urn%3Ali%3Aperson%3A5n_8KatLEt)&sortBy=LAST_MODIFIED'

    headers = {
        'X-Restli-Protocol-Version': '2.0.0',
        'Authorization': 'Bearer ' + access_token,
    }

    response = requests.get(URL, headers=headers)
    print(response.json())
    
