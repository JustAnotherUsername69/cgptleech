import os
import requests
from tqdm import tqdm

def download_file(link: str, user_id: int) -> str:
    """
    Downloads the file from the provided URL and tracks progress.
    Returns the file path once the download is complete.
    """
    # Get the filename from the URL
    filename = os.path.basename(link)
    temp_file_path = f"/tmp/{filename}"  # Path to save the temporary file
    
    # Make the HTTP request to get the file
    response = requests.get(link, stream=True)
    response.raise_for_status()  # Raise an exception for bad responses (e.g., 404)
    
    total_size = int(response.headers.get('Content-Length', 0))  # Get the file size
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True, desc=filename)  # Initialize the progress bar
    
    # Write the file to disk while showing progress
    with open(temp_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):  # Download the file in chunks
            if chunk:
                f.write(chunk)  # Write the chunk to the file
                progress_bar.update(len(chunk))  # Update the progress bar

    progress_bar.close()  # Close the progress bar once done
    return temp_file_path  # Return the path to the downloaded file
