import os
import requests
from tqdm import tqdm

def download_file(link: str, user_id: int) -> str:
    """
    Downloads the file from the link and tracks progress.
    """
    filename = os.path.basename(link)
    temp_file_path = f"/tmp/{filename}"
    
    response = requests.get(link, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('Content-Length', 0))
    
    # Set up a progress bar
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True, desc=filename)
    
    with open(temp_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                progress_bar.update(len(chunk))
    
    progress_bar.close()
    return temp_file_path
