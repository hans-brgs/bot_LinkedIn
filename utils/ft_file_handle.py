from datetime import date
import utils.ft_settings as ft_settings

def get_variable_publication(publication_file):

    with open(publication_file, encoding='utf8') as f:
        contents = f.read()

        # Get "txt" variable
    txt = contents.split("\nmedia=")[0]

    # Get "media" variable
    media = contents.split("\nmedia=")[1].split("\nfile=")[0]
    media = media.replace(" ","")
    media = media.upper()
    if media not in {"VIDEO", "IMAGE", "TEXT", "SHARE", "LINK"} :
        log_error("ERROR_VARIABLE: Please specify \"VIDEO\", \"IMAGE\", \"LINK\", \"SHARE\", or \"TXT\" in the media variable of the text file.")
        return None, None, None
        
    # Get "filename" variable
    if media == "IMAGE" :
        file = contents.split("\nmedia=")[1].split("\nfile=")[1].split("/")
        for x in file :
            if len(x) < 5:
                log_error("ERROR_VARIABLE: Verify the file name \"" + x + "\" in file variable of the text file.")
                return None, None, None
    elif media != "TEXT" :
        file = contents.split("\nmedia=")[1].split("\nfile=")[1]
    else :
        file = None
    
    return txt, media, file

### Check if post is published
def check_publication () :
    with open(ft_settings.history_file, 'r') as f:
        contents = f.readlines()[0:5]
    if date.today().strftime("%d-%m-%Y") in contents[2] :
        return (1)
    else :
        return (0)

#### Save UGCpost history to share later ####

def history(response, txt) :
    response = response.json()
    ugcPost = response["id"].rsplit(":", 1)[1]
    date_publication = date.today().strftime("%d-%m-%Y")
    first_line = txt.split("\n")[0]
    with open(ft_settings.history_file, "r+") as file:
        content = file.read()
        file.seek(0)
        file.write("\n=======================================================================================")
        file.write("\ndate = " + date_publication)
        file.write("\n1st line = " + first_line)
        file.write("\nugcPost = " + ugcPost)
        file.write("\n=======================================================================================\n")
        file.write(content)
        
#### Create Log File    
def log_response(txt, response) :
    with open(ft_settings.log_file, "r+") as file:
        content = file.read()
        file.seek(1)
        file.write(txt)
        file.write(response.text)
        file.write(content) 
        
def log_error(error) :
    with open(ft_settings.log_file, "r+") as file:
        content = file.read()
        file.seek(1)
        file.write(error)
        file.write(content) 
        
