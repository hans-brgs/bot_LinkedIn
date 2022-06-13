import requests
from datetime import date
from utils.ft_file_handle import *
from utils.ft_OAuth import *
from utils.ft_register_media import *
from utils.ft_create_publication import *
from utils.ft_settings import *
from os.path import exists

# Variable
ft_settings.init()
profile_id = <profile_id>
client_id = <client_id>
client_secret = <client_secret>
redirect_url = "https://www.linkedin.com/developers/tools/oauth/redirect"
media_path = "post/media/"
with open(ft_settings.token_file) as f:
    access_token = f.read()
with open(ft_settings.log_file, "r+") as file:
        content = file.read()
        file.seek(0)
        file.write("\n------" + date.today().strftime("%d-%m-%Y") + "------\n")
        file.write(content)

# Check token status
status = None
day_rest = 0
if len(access_token) > 10 :
    day_rest, status = get_token_state(client_id, client_secret, access_token)
while TRUE :
    if (len(access_token) > 10 and status == "active" and day_rest > 7) :
        break
    OAuth_code = get_code_authorization(client_id, redirect_url)
    if OAuth_code == None :
        quit()
    access_token = get_acces_token(
        OAuth_code, redirect_url, client_id, client_secret)
    if access_token == None :
        quit()
    day_rest, status = get_token_state(client_id, client_secret, access_token)

# load file containing publication variables
publication_file = date.today().strftime("%d-%m-%Y") + ".txt"
path_publication = "post/" + publication_file
if not exists(path_publication):
    log_error("ERROR_PUBLICATION_FILE : publication file doesn't exist !")
    quit()
if check_publication() == 1 :
    log_error("ERROR_PUBLICATION_FILE : post has already been published today !")
    quit()
txt, media, file = get_variable_publication(path_publication)
if media == None :
    quit()

# Create a publication according to media type
if media == "VIDEO" :
    upload_URL, digital_media_asset = register_upload_video(access_token, profile_id)
    video_file = media_path + file
    upload_video(upload_URL, video_file, digital_media_asset, access_token)
    response = video_publication(access_token, profile_id, digital_media_asset, txt)
elif media == "IMAGE" :
    list_DMA = []
    for x in file :
        image_file = media_path + x
        upload_URL, digital_media_asset = register_upload_image(access_token, profile_id)
        list_DMA.append(digital_media_asset) 
        upload_image(upload_URL, image_file, access_token)
    response = image_publication(access_token, profile_id, list_DMA, txt)
elif media == "SHARE" :
    response = reshare_publication(access_token, profile_id, file, txt)
elif media == "LINK" :
    response = link_publication(access_token, profile_id, file, txt)
elif media == "TXT" :
    response = text_publication(access_token, profile_id, txt)

if (response.status_code == 201) :
    log_error("✅ SUCCESSFULL PUBLICATION ✅")
else :
    log_error("❌ PUBLICATION FAILURE ❌")
