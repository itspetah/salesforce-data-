import csv
import os
import requests
from requests.exceptions import ConnectionError, HTTPError
from openpyxl import Workbook

# Constants
ATTACHMENT_CSV = 'Attachment.csv'
DOWNLOAD_FOLDER = 'attachments/'
FILE_DOWNLOAD_URL_TEMPLATE = 'https://companyname.file.force.com/servlet/servlet.FileDownload?file='

# Access token
headers = {
    'Authorization': 'Bearer <>'
}

# Ensure the download folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Create a new Excel workbook and sheet
wb = Workbook()
ws = wb.active
ws.title = "File URLs"
ws.append(["File Name", "Downloaded URL"])

# Read the attachment.csv and download the files
with open(ATTACHMENT_CSV, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        file_id = row['Id']
        file_name = row['Name']
        content_type = row['ContentType']
        file_url = FILE_DOWNLOAD_URL_TEMPLATE + file_id

        try:
            response = requests.get(file_url, headers=headers)
            response.raise_for_status()

            # Print debugging info
            print(f"Downloading {file_name}")
            print(f"Content-Type from response: {response.headers.get('Content-Type')}")
            print(f"Expected ContentType from CSV: {content_type}")
            
            print(f"Final URL: {response.url}")
            # check what is the response from api
            print(response.text)
            
            # Check if the file content matches the expected ContentType
            if 'image' in content_type:
                file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: {file_name}")

                # Write the file name and URL to the Excel sheet
                ws.append([file_name, response.url])
            else:
                print(f"Skipped {file_name}, expected image file but got {content_type}")

        except ConnectionError as e:
            print(f"Connection error: {e}")
        except HTTPError as e:
            print(f"HTTP error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Save the Excel file
wb.save('File_URLs.xlsx')
print("Excel file 'File_URLs.xlsx' created with file URLs.")
