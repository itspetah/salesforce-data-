import os
import pandas as pd
import shutil

# Paths
EXPORT_FOLDER = 'path_to_salesforce_export_folder'  # Folder where the export files are located
CSV_FILE = 'file_ids.csv'  # Your CSV file containing File IDs
OUTPUT_FOLDER = 'downloaded_files'  # Folder to save extracted files

# Load CSV
df = pd.read_csv(CSV_FILE)

# Ensure the output folder exists
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Function to extract a file based on ID
def extract_file(file_id, index):
    file_found = False
    for root, dirs, files in os.walk(EXPORT_FOLDER):
        for file in files:
            if file.startswith(file_id):
                file_path = os.path.join(root, file)
                # Handle duplicate names
                dest_file_name = f"{file}"
                dest_file_path = os.path.join(OUTPUT_FOLDER, dest_file_name)
                if os.path.exists(dest_file_path):
                    # Rename if already exists
                    dest_file_name = f"{file_id}_{index}{os.path.splitext(file)[1]}"
                    dest_file_path = os.path.join(OUTPUT_FOLDER, dest_file_name)
                
                shutil.copy(file_path, dest_file_path)
                print(f"Extracted: {dest_file_name}")
                file_found = True
                break
        if file_found:
            break
    if not file_found:
        print(f"File with ID {file_id} not found in the export folder.")

# Loop through the file IDs and extract each file
for index, row in df.iterrows():
    extract_file(row['FileId'], index)

print("Extraction complete.")
