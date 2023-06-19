import logging
import pandas as pd
from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus


def LogAnalyticsQuery():

    # Get the Log Analytics workspace ID and query from the request body
    workspace_id = ""
    #query = "AzureDiagnostics | where ResourceProvider =~'MICROSOFT.KEYVAULT' | where OperationName =='SecretGet' | sort by TimeGenerated"
    query = 'AzureDiagnostics | where ResourceProvider =~"MICROSOFT.KEYVAULT" | where OperationName =="SecretGet" |where identity_claim_scp_s == "user_impersonation" | project KeyVault = Resource, Username = identity_claim_unique_name_s, TimeGenerated, OperationName, SecretName= tostring(split(requestUri_s,"/",4)) | sort by TimeGenerated'

    # Authenticate using DefaultAzureCredential
    credential = DefaultAzureCredential()

    try:
        # Create a LogsQueryClient
        client = LogsQueryClient(credential)

        # Execute the query
        start_time = datetime.today() - timedelta(days=7)
        end_time = datetime.today()

        # Run the Log Analytics query
        result = client.query_workspace(workspace_id, query, timespan=(start_time, end_time))
        
        if result.status == LogsQueryStatus.PARTIAL:
            error = result.partial_error
            data = result.partial_data
            logging.error(error)
        elif result.status == LogsQueryStatus.SUCCESS:
            data = result.tables

        for table in data:
            df = pd.DataFrame(data=table.rows, columns=table.columns).to_html
            logging.info(df)
            #df.to_html("test.html")

        return df

    except Exception as e:
        logging.error(f'Failed to execute Log Analytics query: {str(e)}')
        return 'Failed to execute Log Analytics query'
