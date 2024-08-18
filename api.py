import requests
import csv

# Salesforce API details
instance_url = 'https://yourInstance.salesforce.com'
access_token = 'YOUR_ACCESS_TOKEN'

# Read leads and attachments data
with open('leads.csv', 'r') as leads_file:
    leads_data = csv.DictReader(leads_file)
    leads_map = {row['Lead ID']: row['Lead Name'] for row in leads_data}

with open('attachments.csv', 'r') as attachments_file:
    attachments_data = csv.DictReader(attachments_file)
    for attachment in attachments_data:
        lead_id = attachment['ParentId']
        file_name = leads_map.get(lead_id, 'Unknown') + '.' + attachment['ContentType']
        file_url = instance_url + '/services/data/vXX.0/sobjects/Attachment/' + attachment['Id'] + '/Body'
        
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        
        response = requests.get(file_url, headers=headers)
        
        if response.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to download {file_name}")

