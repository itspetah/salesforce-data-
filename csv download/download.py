import csv
import requests
import os

def download_file(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure we notice bad responses
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {filename}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # HTTP error
    except Exception as err:
        print(f"Other error occurred: {err}")  # Other errors

def main():
    csv_filename = 'files.csv'
    download_dir = 'downloaded_files'

    # Create download directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            file_url = row['ContentDownloadUrl']
            file_name = row['Title'] + '.' + row['FileExtension']
            file_path = os.path.join(download_dir, file_name)
            download_file(file_url, file_path)

if __name__ == "__main__":
    main()
