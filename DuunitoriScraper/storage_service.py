from azure.data.tables import TableServiceClient
import logging
from DuunitoriScraper.data_models import JobPosting


def store_postings(postings: list[JobPosting]):
    #TODO generate new connection string and use env variable
    table_service_client = TableServiceClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;AccountName=jobpostingevents;AccountKey=NKyU9y+OTgp6Y1XvFX45fUvhko6gcjZqAkM4Am8E/0Rh4Ae8UM31O0hk6kK1wGItLscYdJxTdy5U+AStlu1cpQ==;EndpointSuffix=core.windows.net")
    table_client = table_service_client.get_table_client(table_name="Postings")

    failure_count = 0
    for i in postings:
        try:
            json_entity = vars(i)
            json_entity['PartitionKey'] = i.company
            json_entity['RowKey']= i.job_id
        
            table_client.create_entity(entity=json_entity)
        except Exception as e :
            failure_count += 1
            logging.exception(f"Adding entity: {i.job_id} failed. Reason: {e.with_traceback}")
    logging.info(f"Added {len(postings) - failure_count} elements to database.")