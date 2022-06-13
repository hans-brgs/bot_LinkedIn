from pickle import TRUE
from time import sleep
import requests
from utils.ft_file_handle import log_response

#### VIDEO UPLOAD ####

def register_upload_video(access_token, profile_id):

    URL = 'https://api.linkedin.com/v2/assets'

    # request's ARGS
    headers = {'Content-Type': 'application/json',
               'X-Restli-Protocol-Version': '2.0.0',
               'Authorization': 'Bearer ' + access_token}
    params = {
        'action': 'registerUpload',
    }
    json_data = {
        'registerUploadRequest': {
            'owner': 'urn:li:person:' + profile_id,
            'recipes': [
                'urn:li:digitalmediaRecipe:feedshare-video',
            ],
            'serviceRelationships': [
                {
                    'identifier': 'urn:li:userGeneratedContent',
                    'relationshipType': 'OWNER',
                },
            ],
        },
    }

    # POST request
    response = requests.post(URL,
                             params=params, headers=headers, json=json_data)
    log_response("REGISTER_VIDEO_UPLOAD_RESPONSE : ", response)
    response = response.json()

    # response's variables
    upload_URL = response["value"]["uploadMechanism"]['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
    digital_media_asset = response["value"]["asset"]
    digital_media_asset = digital_media_asset.rsplit(":", 1)[1]
    return upload_URL, digital_media_asset


def wait_status_upload(digital_media_asset, access_token):

    URL = "https://api.linkedin.com/v2/assets/"

    # request's ARGS
    headers = {'Authorization': 'Bearer ' + access_token}

    # Wait until the video has finished uploading
    while TRUE:
        response = requests.get(URL + digital_media_asset, headers=headers)
        response = response.json()
        status = response["recipes"][0]["status"]
        if status == "AVAILABLE":
            break
        elif status != "PROCESSING" and status != "WAITING_UPLOAD":
            break
        sleep(1)
    return status


def upload_video(upload_URL, video_file, digital_media_asset, access_token):

    # request's ARGS
    headers = {
        'Content-Type': 'application/octet-stream',
    }

    with open(video_file, 'rb') as f:
        data = f.read()
    response = requests.put(upload_URL, headers=headers, data=data)
    log_response("VIDEO_UPLOAD_RESPONSE : ", response)
    wait_status_upload(digital_media_asset, access_token)

#### IMAGE UPLOAD ####
def register_upload_image(access_token, profile_id):

    URL = 'https://api.linkedin.com/v2/assets'

    # request's ARGS
    headers = {'Content-Type': 'application/json',
               'X-Restli-Protocol-Version': '2.0.0',
               'Authorization': 'Bearer ' + access_token}
    params = {
        'action': 'registerUpload',
    }
    json_data = {
        'registerUploadRequest': {
            'owner': 'urn:li:person:' + profile_id,
            'recipes': [
                'urn:li:digitalmediaRecipe:feedshare-image',
            ],
            'serviceRelationships': [
                {
                    'identifier': 'urn:li:userGeneratedContent',
                    'relationshipType': 'OWNER',
                },
            ],
            "supportedUploadMechanism": [
                "SYNCHRONOUS_UPLOAD"
            ]
        },
    }

    # POST request
    response = requests.post(URL,
                             params=params, headers=headers, json=json_data)
    log_response("REGISTER_IMAGE_UPLOAD_RESPONSE : ", response)
    response = response.json()

    # response's variables
    upload_URL = response["value"]["uploadMechanism"]['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
    digital_media_asset = response["value"]["asset"]
    digital_media_asset = digital_media_asset.rsplit(":", 1)[1]
    return upload_URL, digital_media_asset


def upload_image(upload_URL, image_file, access_token):

    # request's ARGS
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }

    with open(image_file, 'rb') as f:
        data = f.read()
    response = requests.put(upload_URL, headers=headers, data=data)
    log_response("IMAGE_UPLOAD_RESPONSE : ", response)
