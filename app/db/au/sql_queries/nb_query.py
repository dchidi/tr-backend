# nb_fit_query = """
#         SELECT * FROM (SELECT 
#     CONVERT(DATE, PT.CreatedDate) AS created_at,
#     'AU' AS country,
#     CASE 
#         WHEN Q.QuoteSaveFrom = 1 THEN 'Phone'
#         WHEN Q.QuoteSaveFrom = 2 THEN 'Web'
#         ELSE 'Other'
#     END AS receivedMethod,
#     COUNT(P.PolicyNumber) AS sales_count, '' AS product, 'FIT' as [system]
# FROM [fit-petcover].[dbo].PolicyTransaction PT
# INNER JOIN [fit-petcover].[dbo].Policy P ON P.Id = PT.PolicyId
# INNER JOIN [fit-petcover].[dbo].Quote Q ON Q.Id = PT.QuoteId) T
# WHERE 
#     CONVERT(DATE, PT.CreatedDate) >= :start_date
#     AND CONVERT(DATE, PT.CreatedDate) < :end_date
#     AND PT.TransactionTypeId = 1
#     AND ISNULL(P.IsFreeProduct, 0) = 0
#     AND P.PolicyStatusId = (SELECT Id FROM [fit-petcover].[dbo].PolicyStatus WHERE Name = 'Active')
#     AND ISNULL(P.PetName, '') NOT LIKE '%test%'
#     AND P.PolicyNumber NOT LIKE '%TEST%'
# GROUP BY 
#     CONVERT(DATE, PT.CreatedDate),
#     CASE 
#         WHEN Q.QuoteSaveFrom = 1 THEN 'Phone'
#         WHEN Q.QuoteSaveFrom = 2 THEN 'Web'
#         ELSE 'Other'
#     END
#         """
nb_fit_query = """
SELECT 
    T.created_at,
    T.receivedMethod,
    SUM(T.sales_count) AS sales_count,
    'FIT' as [system],
	'AU' as country
FROM (
    SELECT 
        CONVERT(DATE, PT.CreatedDate) AS created_at,
        'AU' AS country,
        CASE 
            WHEN Q.QuoteSaveFrom = 1 THEN 'Phone'
            WHEN Q.QuoteSaveFrom = 2 THEN 'Web'
            ELSE 'Other'
        END AS receivedMethod,
        COUNT(P.PolicyNumber) AS sales_count,
        '' AS product,
        'Petcover' AS [system]
    FROM [fit-petcover].[dbo].PolicyTransaction PT
    INNER JOIN [fit-petcover].[dbo].Policy P ON P.Id = PT.PolicyId
    INNER JOIN [fit-petcover].[dbo].Quote Q ON Q.Id = PT.QuoteId
    WHERE  
        PT.TransactionTypeId = 1
        AND ISNULL(P.IsFreeProduct, 0) = 0
        AND P.PolicyStatusId = (
            SELECT Id 
            FROM [fit-petcover].[dbo].PolicyStatus 
            WHERE Name = 'Active'
        )
        AND ISNULL(P.PetName, '') NOT LIKE '%test%'
        AND P.PolicyNumber NOT LIKE '%TEST%'
    GROUP BY 
        CONVERT(DATE, PT.CreatedDate),
        Q.QuoteSaveFrom

    UNION ALL

    SELECT 
        CONVERT(DATE, PT.CreatedDate) AS created_at,
        'AU' AS country,
        CASE 
            WHEN Q.QuoteSaveFrom = 1 THEN 'Phone'
            WHEN Q.QuoteSaveFrom = 2 THEN 'Web'
            ELSE 'Other'
        END AS receivedMethod,
        COUNT(P.PolicyNumber) AS sales_count,
        '' AS product,
        'FIT' AS [system]
    FROM [FIT_DATA].[dbo].PolicyTransaction PT
    INNER JOIN [FIT_DATA].[dbo].Policy P ON P.Id = PT.PolicyId
    INNER JOIN [FIT_DATA].[dbo].Quote Q ON Q.Id = PT.QuoteId
    WHERE  
        PT.TransactionTypeId = 1
        AND ISNULL(P.IsFreeProduct, 0) = 0
        AND P.PolicyStatusId = (
            SELECT Id 
            FROM [fit-petcover].[dbo].PolicyStatus 
            WHERE Name = 'Active'
        )
        AND ISNULL(P.PetName, '') NOT LIKE '%test%'
        AND P.PolicyNumber NOT LIKE '%TEST%'
    GROUP BY 
        CONVERT(DATE, PT.CreatedDate),
        Q.QuoteSaveFrom
) T
WHERE 
    T.created_at >= :start_date
    AND T.created_at < :end_date
GROUP BY 
    T.created_at,
    T.receivedMethod,
    T.system
ORDER BY 
    T.created_at ASC,
    T.receivedMethod ASC;
"""
nb_uts_query = """
    SELECT
        created_at,
        receivedMethod,
        country,
        COUNT(PolicyNumber) AS sales_count,'' AS product, 'UTS' as [system]
    FROM (
        SELECT
            PO.ProductCode,
            PO.ProductName,
            TT.TransactionTypeName,
            TT.Id AS TransactionTypeId,
            PA.TotalPremiumAmount,
            0 AS [IsPetIdProduct],
            PA.StartDate,
            CONVERT(DATE, PA.CreatedDate) AS created_at,
            P.PolicyNumber,
            P.PetName,
            CL.FirstName AS ClientName,
            P.IsFreeProduct,
            CASE
                WHEN U.FirstName IN ('FIT', 'Web') THEN 'Web'
                ELSE 'Phone'
            END AS receivedMethod,
            'UTS1' AS [System],
            PS.PolicyStatusName,
            'AU' AS country
        FROM [PolicyActivity] PA
        LEFT JOIN Policy P ON P.Id = PA.PolicyId
        LEFT JOIN [Master].[PolicyStatus] PS ON PS.Id = P.PolicyStatusId
        INNER JOIN [Master].[TransactionType] TT ON TT.Id = PA.TransactionTypeId
        INNER JOIN [dbo].[Product] PO ON PO.Id = PA.ProductId
        LEFT JOIN Client CL ON CL.Id = P.ClientId
        LEFT JOIN [dbo].[User] U ON P.ExecutiveId = U.Id
        WHERE
            CONVERT(DATE, PA.CreatedDate) >= :start_date
            AND CONVERT(DATE, PA.CreatedDate) < :end_date
            AND PA.TransactionTypeId = 1
            AND ISNULL(CL.FirstName, '') NOT LIKE '%Test%'
            AND ISNULL(P.PetName, '') NOT LIKE '%test%'
            AND P.PolicyNumber NOT LIKE '%TEST%'
            AND PS.PolicyStatusName = 'Active'
            AND ISNULL(P.IsFreeProduct, 0) = 0
            AND PO.ProductCode NOT LIKE '%CM%'
    ) AS FilteredData
    GROUP BY
        receivedMethod,
        country, created_at
"""
