import os
import pandas as pd
import requests
from requests_oauthlib import OAuth2Session
from simple_salesforce import Salesforce

# Salesforce credentials
CONSUMER_KEY = 'your_consumer_key'
CONSUMER_SECRET = 'your_consumer_secret'
REDIRECT_URI = 'http://localhost:8888/callback'  # Adjusted to match Jupyter Lab port
AUTH_URL = 'https://login.salesforce.com/services/oauth2/authorize'
TOKEN_URL = 'https://login.salesforce.com/services/oauth2/token'

# CSV file containing Salesforce File IDs
CSV_FILE = 'file_ids.csv'

# Directory to save the downloaded files
DOWNLOAD_DIR = 'downloaded_files'

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Function to handle OAuth2 authorization
def get_salesforce_token():
    salesforce = OAuth2Session(CONSUMER_KEY, redirect_uri=REDIRECT_URI)
    authorization_url, state = salesforce.authorization_url(AUTH_URL)
    print('Please go to this URL and authorize access:', authorization_url)

    # Get the authorization verifier code from the callback URL
    redirect_response = input('Paste the full callback URL here: ')
    salesforce.fetch_token(TOKEN_URL, authorization_response=redirect_response, client_secret=CONSUMER_SECRET)
    
    return salesforce.token

# Get the OAuth token
token = get_salesforce_token()

# Create a session with the token
sf = Salesforce(instance_url=token['instance_url'], session_id=token['access_token'])

# Read the CSV file
df = pd.read_csv(CSV_FILE)

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
    response = requests.get(f"{token['instance_url']}{file_data['VersionData']}", headers={"Authorization": f"Bearer {token['access_token']}"})
    
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
