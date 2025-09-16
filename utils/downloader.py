import os
import requests
from tqdm import tqdm

async def download_file(link: str, user_id: int) -> str:
    """
    Downloads the file from the provided URL and tracks progress.
    Returns the file path once the download is complete.
    """
    filename = os.path.basename(link)
    temp_file_path = f"/tmp/{filename}"
    
    # Perform HTTP request to download the file
    response = requests.get(link, stream=True)
    response.raise_for_status()  # Ensure no errors occurred
    
    total_size = int(response.headers.get('Content-Length', 0))  # Get the file size
    
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True, desc=filename)
    
    with open(temp_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)  # Write chunk to the temporary file
                progress_bar.update(len(chunk))  # Update progress bar
        
    progress_bar.close()  # Close the progress bar once done
    return temp_file_path  # Return path to the downloaded file
