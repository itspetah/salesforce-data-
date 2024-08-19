import pandas as pd
import base64
import os

# Load the CSV file (adjust the filename as needed)
csv_file = "ContentVersion.csv"  # or "Attachment.csv"
df = pd.read_csv(csv_file)

# Specify the columns that contain file data and file names
data_column = 'VersionData'  # for ContentVersion
# data_column = 'Body'  # for Attachment

filename_column = 'Title'  # for ContentVersion
# filename_column = 'Name'  # for Attachment

# Create an output directory for the images
output_dir = 'extracted_images'
os.makedirs(output_dir, exist_ok=True)

# Iterate over each row in the CSV file
for index, row in df.iterrows():
    # Extract the file data and name
    file_data = row[data_column]
    file_name = row[filename_column]
    
    # Decode the Base64 encoded data
    file_bytes = base64.b64decode(file_data)
    
    # Write the file to the output directory
    output_path = os.path.join(output_dir, file_name)
    with open(output_path, 'wb') as file:
        file.write(file_bytes)
    
    print(f"Extracted: {file_name}")

print("Extraction complete.")
