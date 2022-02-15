import os
import requests

from pathvalidate import sanitize_filepath
from redirect import check_for_redirect

def download_txt(book_url, txt_filename, txt_filepath):
    os.makedirs(txt_filepath, exist_ok=True)
    response = requests.get(book_url)
    response.raise_for_status()
    check_for_redirect(response)
    txt_filename = sanitize_filepath(txt_filename)
    filepath = os.path.join(txt_filepath, txt_filename)
    with open(filepath, 'w')as file:
        file.write(response.text)
