import os
import requests
from tqdm import tqdm

def download_files_from_ftp(url, local_directory):
    try:
        # Send a GET request to the FTP server URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful

        # Parse the HTML response to extract the file names
        file_names = []
        lines = response.text.split('\n')
        for line in lines:
            if line.startswith('<a href="'):
                file_name = line.split('"')[1]
                file_names.append(file_name)

        # Download each file with progress using tqdm
        with tqdm(total=len(file_names), unit='file') as pbar_files:
            for file_name in file_names:
                pbar_files.set_description(f"Processing {file_name}")
                file_url = url + file_name
                local_file_path = os.path.join(local_directory, file_name)
                
                # Check if file already exists
                if not os.path.exists(local_file_path):
                    response = requests.get(file_url, stream=True)
                    response.raise_for_status()
                    total_size = int(response.headers.get('Content-Length', 0))

                    with open(local_file_path, 'wb') as local_file, tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024, leave=False) as pbar_download:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                local_file.write(chunk)
                                pbar_download.update(len(chunk))
                pbar_files.update()

        print('Download complete!')

    except Exception as e:
        print('An error occurred:', str(e))

# Provide the FTP server URL and local directory path to save the files
ftp_url = 'https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/XML/'
local_directory = './compounds/'

# Call the function to download the files
download_files_from_ftp(ftp_url, local_directory)

