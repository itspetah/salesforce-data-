import pandas as pd

# Load the CSV files
attachments_df = pd.read_csv('Attachment.csv')  # or ContentVersion.csv
leads_df = pd.read_csv('Lead.csv')

# Merge the two dataframes based on the matching IDs
merged_df = pd.merge(attachments_df, leads_df, how='left', left_on='ParentId', right_on='Id')

# Save the mapping to a new CSV file
merged_df.to_csv('File_Lead_Mapping.csv', index=False)

print("Mapping complete. Check File_Lead_Mapping.csv for results.")
