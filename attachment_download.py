import csv
import os
import requests

# Constants
ATTACHMENT_CSV = 'attachment.csv'
DOWNLOAD_FOLDER = 'attachments/'
FILE_DOWNLOAD_URL_TEMPLATE = 'https://your-salesforce-instance.com/servlet/servlet.FileDownload?file='  # Replace with actual Salesforce URL template

# Ensure the download folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Read the attachment.csv and download the files
with open(ATTACHMENT_CSV, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        file_id = row['Id']
        file_name = row['Name']
        file_url = FILE_DOWNLOAD_URL_TEMPLATE + file_id

        response = requests.get(file_url)
        
        if response.status_code == 200:
            file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {file_name}")
        else:
            print(f"Failed to download {file_name} from {file_url}")
