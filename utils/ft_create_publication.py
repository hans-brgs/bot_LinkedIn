import requests
from utils.ft_file_handle import history, log_response
import utils.ft_settings as ft_settings

#### PUBLICATION ####
def text_publication(access_token, profile_id, txt):

    URL = "https://api.linkedin.com/v2/ugcPosts"

    # request's ARGS
    headers = {'Content-Type': 'application/json',
               'X-Restli-Protocol-Version': '2.0.0',
               'Authorization': 'Bearer ' + access_token}
    post_data = {
        "author": "urn:li:person:" + profile_id,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": txt,
                },
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"
        }
    }
    response = requests.post(URL, headers=headers, json=post_data)
    log_response("TXT_PUBLICATION_REPONSE : ", response)

    if response.status_code == 201:
        history(response, txt)

    return(response)


def reshare_publication(access_token, profile_id, URN, txt):

    URL = "https://api.linkedin.com/v2/ugcPosts"

    # request's ARGS
    headers = {'Content-Type': 'application/json',
               'X-Restli-Protocol-Version': '2.0.0',
               'Authorization': 'Bearer ' + access_token}
    post_data = {
        "lifecycleState": "PUBLISHED",
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        },
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareMediaCategory": "NONE",
                "shareCommentary": {
                    "text": txt
                },
                "media": [],
                "shareCategorization": {}
            }
        },
        "author": "urn:li:person:" + profile_id,
        "responseContext": {
            "parent": "urn:li:ugcPost:" + URN,
        }
    }
    response = requests.post(URL, headers=headers, json=post_data)
    log_response("RESHARE_PUBLICATION_REPONSE : ", response)

    if response.status_code == 201:
        history(response, txt)

    return(response)


def video_publication(access_token, profile_id, digital_media_asset, txt):

    URL = "https://api.linkedin.com/v2/ugcPosts"

    # request's ARGS
    headers = {'Content-Type': 'application/json',
               'X-Restli-Protocol-Version': '2.0.0',
               'Authorization': 'Bearer ' + access_token}

    post_data = {
        "author": "urn:li:person:" + profile_id,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "media": [
                    {
                        "media": "urn:li:digitalmediaAsset:" + digital_media_asset,
                        "status": "READY",
                    }
                ],
                "shareCommentary": {
                    "attributes": [],
                    "text": txt
                },
                "shareMediaCategory": "VIDEO"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"
        }
    }
    response = requests.post(URL, headers=headers, json=post_data)
    log_response("VIDEO_PUBLICATION_RESPONSE : ", response)

    if response.status_code == 201:
        history(response, txt)

    return(response)


def image_publication(access_token, profile_id, digital_media_asset, txt):

    URL = "https://api.linkedin.com/v2/ugcPosts"

    # request's ARGS
    headers = {'Content-Type': 'application/json',
               'X-Restli-Protocol-Version': '2.0.0',
               'Authorization': 'Bearer ' + access_token}

    media = []
    for x in digital_media_asset:
        Dict = {
            "media": "urn:li:digitalmediaAsset:" + x,
            "status": "READY",
            "title": {
                "attributes": [],
                "text": ""
            }
        }
        media.append(Dict)

    post_data = {
        "author": "urn:li:person:" + profile_id,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "media": media,
                "shareCommentary": {
                    "attributes": [],
                    "text": txt
                },
                "shareMediaCategory": "IMAGE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"
        }
    }
    response = requests.post(URL, headers=headers, json=post_data)
    log_response("IMAGE_PUBLICATION_RESPONSE : ", response)

    if response.status_code == 201:
        history(response, txt)

    return(response)


def link_publication(access_token, profile_id, LINK, txt):

    URL = "https://api.linkedin.com/v2/ugcPosts"

    # request's ARGS
    headers = {'Content-Type': 'application/json',
               'X-Restli-Protocol-Version': '2.0.0',
               'Authorization': 'Bearer ' + access_token}
    post_data = {
        "author": "urn:li:person:" + profile_id,
        "lifecycleState": "PUBLISHED",
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        },
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareMediaCategory": "ARTICLE",
                "shareCommentary": {
                    "text": txt
                },
                "media": [
                    {
                        "originalUrl":  LINK,
                        "status": "READY",
                    }
                ],
            }
        },
    }
    response = requests.post(URL, headers=headers, json=post_data)
    log_response("LINK_PUBLICATION_RESPONSE : ", response)

    if response.status_code == 201:
        history(response, txt)

    return(response)
