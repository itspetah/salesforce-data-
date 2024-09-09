import csv
import os
import requests
from requests.exceptions import ConnectionError, HTTPError
from bs4 import BeautifulSoup

# Constants
ATTACHMENT_CSV = 'All_Files.csv'
DOWNLOAD_FOLDER = 'attachments/'
FILE_VIEW_URL_TEMPLATE = 'https://companyname.lightning.force.com/lightning/r/ContentDocument/'

# Access token
headers = {
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
}

# Ensure the download folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Function to get the download URL from the view page
def get_download_url(view_url):
    try:
        response = requests.get(view_url, headers=headers)
        response.raise_for_status()
        
        # Parse HTML to find the download URL
        soup = BeautifulSoup(response.text, 'html.parser')
        # Example: Locate the download link
        download_link = soup.find('a', {'id': 'download-button'})  # Adjust selector to match your HTML
        if download_link and 'href' in download_link.attrs:
            return download_link.attrs['href']
        
    except ConnectionError as e:
        print(f"Connection error while getting download URL: {e}")
    except HTTPError as e:
        print(f"HTTP error while getting download URL: {e}")
    return None

# Read the attachment.csv and download the files
with open(ATTACHMENT_CSV, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        file_id = row['Id']
        file_name = row['Title']
        file_extension = row.get('FileExtension', '')
        file_name = f"{file_name}.{file_extension}" if file_extension else file_name
        view_url = FILE_VIEW_URL_TEMPLATE + file_id + "/view"

        try:
            # Get the download URL from the view page
            download_url = get_download_url(view_url)
            if download_url:
                response = requests.get(download_url, headers=headers)
                response.raise_for_status()

                # Print debugging info
                print(f"Downloading {file_name}")
                print(f"Final URL: {response.url}")

                # Write the content to a file
                file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: {file_name}")
            else:
                print(f"Download URL not found for file ID {file_id}")

        except ConnectionError as e:
            print(f"Connection error: {e}")
        except HTTPError as e:
            print(f"HTTP error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
