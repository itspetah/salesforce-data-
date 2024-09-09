# Download Salesforce Files

## USe SOQL to query necessary fields from Table ContentDocument using WorkBench
```sql
SELECT FileExtension,FileType,Id,LatestPublishedVersionId,Title FROM ContentDocument
```
## Export the query using option Bulk CSV
Extract File and run script
Extract.py

## Tip: Following URL to open and download the file
https://conedison.file.force.com/sfc/servlet.shepherd/version/download/LatestPublishedVersionId
```txt
Example: https://conedison.file.force.com/sfc/servlet.shepherd/version/download/0681W00000It0S1
```
