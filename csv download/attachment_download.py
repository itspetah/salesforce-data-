import csv
import os
import requests
from requests.exceptions import ConnectionError, HTTPError

# Constants
ATTACHMENT_CSV = 'All_Files.csv'
DOWNLOAD_FOLDER = 'attachments/'
FILE_DOWNLOAD_URL_TEMPLATE = 'https://companyname.lightning.force.com/lightning/r/ContentDocument/'

# Access token
headers = {
    'Authorization': 'Bearer <>'
}

# Ensure the download folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Read the attachment.csv and download the files
with open(ATTACHMENT_CSV, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        file_id = row['Id']
        file_name = row['Title']
        content_type = row['FileExtension']
        file_url = FILE_DOWNLOAD_URL_TEMPLATE + file_id + "/view"

        try:
            response = requests.get(file_url, headers=headers)
            response.raise_for_status()

            # Print debugging info
            print(f"Downloading {file_name}")
            print(f"Final URL: {response.url}")
            
            # check what is the response from api
            # print(response.text)
            
            # Check if the file content matches the expected ContentType
            
            file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {file_name}")

        except ConnectionError as e:
            print(f"Connection error: {e}")
        except HTTPError as e:
            print(f"HTTP error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
