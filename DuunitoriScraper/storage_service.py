from azure.data.tables import TableServiceClient

def store_postings(postings):
    #TODO generate new connection string and use env variable
    table_service_client = TableServiceClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;AccountName=jobpostingevents;AccountKey=NKyU9y+OTgp6Y1XvFX45fUvhko6gcjZqAkM4Am8E/0Rh4Ae8UM31O0hk6kK1wGItLscYdJxTdy5U+AStlu1cpQ==;EndpointSuffix=core.windows.net")
    table_client = table_service_client.get_table_client(table_name="Postings")
    for i in postings:
        try:
            json_entity = vars(i)
            json_entity['PartitionKey'] = i.company
            json_entity['RowKey']= i.job_id
        
            table_client.create_entity(entity=json_entity)
        except Exception as e :
            print(e)