import os
import pandas as pd
import requests
from simple_salesforce import Salesforce

# Salesforce credentials
USERNAME = 'your_username'
PASSWORD = 'your_password'
SECURITY_TOKEN = 'your_security_token'
INSTANCE_URL = 'https://your_instance.salesforce.com'

# CSV file containing Salesforce File IDs
CSV_FILE = 'file_ids.csv'

# Directory to save the downloaded files
DOWNLOAD_DIR = 'downloaded_files'

# Connect to Salesforce
sf = Salesforce(username=USERNAME, password=PASSWORD, security_token=SECURITY_TOKEN, instance_url=INSTANCE_URL)

# Read the CSV file
df = pd.read_csv(CSV_FILE)

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Function to download a file
def download_file(file_id, index):
    # Query the ContentVersion to get the file details
    query = f"SELECT Title, FileExtension, VersionData FROM ContentVersion WHERE Id = '{file_id}'"
    result = sf.query(query)

    if not result['records']:
        print(f"No file found for File ID {file_id}")
        return

    file_data = result['records'][0]
    file_name = f"{file_data['Title']}.{file_data['FileExtension']}"
    
    # Check if file name already exists
    file_path = os.path.join(DOWNLOAD_DIR, file_name)
    if os.path.exists(file_path):
        # Rename the file if a file with the same name exists
        file_name = f"{file_data['Title']}_{index}.{file_data['FileExtension']}"
        file_path = os.path.join(DOWNLOAD_DIR, file_name)
    
    # Download the file content
    response = requests.get(f"{INSTANCE_URL}{file_data['VersionData']}", headers={"Authorization": f"Bearer {sf.session_id}"})
    
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_name}")
    else:
        print(f"Failed to download file {file_id}")

# Loop through the file IDs and download each file
for index, row in df.iterrows():
    download_file(row['FileId'], index)

print("Download complete.")
