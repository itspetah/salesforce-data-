import csv
import os

# Constants
ATTACHMENT_CSV = 'attachment.csv'
DOWNLOAD_FOLDER = 'attachments/'

# Ensure the download folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Read the attachment.csv and save files based on ContentType
with open(ATTACHMENT_CSV, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        file_id = row['Id']
        file_name = row['Name']
        content_type = row['ContentType']  # Get ContentType from CSV

        # Simulate file content retrieval (in a real scenario, retrieve content from Salesforce)
        file_content = b''  # Replace with actual file content retrieval logic

        # Print debugging info
        print(f"Processing {file_name}")
        print(f"Expected ContentType from CSV: {content_type}")

        if 'image' in content_type:
            file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
            with open(file_path, 'wb') as f:
                f.write(file_content)
            print(f"Saved: {file_name}")
        else:
            print(f"Skipped {file_name}, expected image file but got {content_type}")
