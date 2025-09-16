import os
import requests

def download_file(link: str) -> str:
    """
    Downloads the file from the link and returns the path to the downloaded file.
    """
    filename = os.path.basename(link)
    temp_file_path = f"/tmp/{filename}"
    
    response = requests.get(link, stream=True)
    response.raise_for_status()
    
    with open(temp_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    
    return temp_file_path
