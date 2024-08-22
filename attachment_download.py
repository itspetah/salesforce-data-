import csv
import os
import requests
from requests.exceptions import ConnectionError, HTTPError

# Constants
ATTACHMENT_CSV = 'attachment.csv'
DOWNLOAD_FOLDER = 'attachments/'
FILE_DOWNLOAD_URL_TEMPLATE = 'https://companyname.lightning.force.com/servlet/servlet.FileDownload?file='  # Your Salesforce domain

# Optionally, include headers if authentication is needed
# Replace <Your-Access-Token> with your actual Salesforce access token
headers = {
    'Authorization': 'Bearer <Your-Access-Token>'
}

# Ensure the download folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Read the attachment.csv and download the files
with open(ATTACHMENT_CSV, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        file_id = row['Id']
        file_name = row['Name']
        file_url = FILE_DOWNLOAD_URL_TEMPLATE + file_id

        try:
            response = requests.get(file_url, headers=headers)
            response.raise_for_status()  # Raises an error for bad responses

            # Print content type for debugging
            print(f"Downloading {file_name}, Content-Type: {response.headers.get('Content-Type')}")

            # Check if the response is HTML (indicating a potential problem)
            if 'text/html' in response.headers.get('Content-Type', ''):
                print(f"Warning: Received HTML content instead of the expected file for {file_name}.")
                continue

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
