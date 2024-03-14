import os
import requests

def download_file(url, destination_folder, file_name):
    """
    Download a file from a specified URL into a given destination folder with a specific file name.

    :param url: URL of the file to download.
    :param destination_folder: Folder where the file should be saved.
    :param file_name: Name of the file to save the download as.
    """
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Full path to save the file
    file_path = os.path.join(destination_folder, file_name)

    # Downloading the file
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"File downloaded successfully and saved as {file_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

if __name__ == "__main__":
    # URL of the dataset to download
    dataset_url = "https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-52/botnet-capture-20110818-bot-2.pcap"

    # Path to save the downloaded file
    # Adjust the path according to your project structure, assuming this script is run from src/data
    destination_path = "../../data/raw"

    # Name of the file to save as
    file_name = "testing.pcap"

    download_file(dataset_url, destination_path, file_name)
