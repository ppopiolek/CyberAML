import requests
import zipfile
import os

def download_and_extract(url, extract_to):
    # Create the directory if it does not exist
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    
    # Set the local file path, stripping the query string for simplicity
    local_filename = os.path.join(extract_to, os.path.basename(url).split('?')[0] + '.zip')

    # Download the file
    with requests.get(url, stream=True) as r:
        if r.status_code == 200:
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):  # Download the file in chunks
                    f.write(chunk)
            print("Download completed successfully.")
        else:
            print(f"Failed to download. Status code: {r.status_code}")
            return
    
    # Attempt to unzip the file
    try:
        with zipfile.ZipFile(local_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_to)  # Extract all the contents into the specified directory
            print("Extraction completed successfully.")
    except zipfile.BadZipFile:
        print("Failed to unzip: The file is not a zip file.")
    
    # Remove the zip file after extraction
    os.remove(local_filename)

# Example WeTransfer URL (please update to a working link)
we_transfer_url = "https://download.wetransfer.com/eugv/8b029253772896a1fa0f79a6c2452afc20240420085634/5fda4da5e81f9e879918f7d20aaa906ddef6eea4/raw.zip?cf=y&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRlZmF1bHQifQ.eyJleHAiOjE3MTQxMzc2MjMsImlhdCI6MTcxNDEzNzAyMywiZG93bmxvYWRfaWQiOiI4ZjFlYzdiYy1kMzkzLTQ1MTgtODlkOS1mNjY3NTlmMGRlOGIiLCJzdG9yYWdlX3NlcnZpY2UiOiJzdG9ybSJ9.iZbXqx0QuAJJ7RArRXZWhN4U_pH6O5STg7Fmi_UgiUw"

# Path to the directory where the file will be saved and extracted
output_directory = "../../data/raw"

download_and_extract(we_transfer_url, output_directory)
