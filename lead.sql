SELECT
    ContentDocument.Id,
    ContentDocument.Title,
    ContentDocument.ContentSize,
    ContentDocument.FileExtension,
    Lead.Name
FROM
    ContentDocument
    INNER JOIN ContentDocumentLink ON ContentDocument.Id = ContentDocumentLink.ContentDocumentId
    INNER JOIN Lead ON ContentDocumentLink.LinkedEntityId = Lead.Id
WHERE
    ContentDocumentLink.LinkedEntityId IN (SELECT Id FROM Lead)
