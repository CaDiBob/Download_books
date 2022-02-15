import os
import requests

from redirect import check_for_redirect

def download_image(img_url, img_filename, img_filepath):
    os.makedirs(img_filepath, exist_ok=True)
    response = requests.get(img_url)
    response.raise_for_status()
    check_for_redirect(response)
    filepath = os.path.join(img_filepath, img_filename)
    with open(filepath, 'wb')as file:
        file.write(response.content)